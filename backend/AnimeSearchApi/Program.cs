using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using Microsoft.ML.Tokenizers;
using Qdrant.Client;
using Qdrant.Client.Grpc;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();

// allow the browser to call this api
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
        policy.WithOrigins("http://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod());
});

// making onnx model, tokenizer and qdrant as singletons
builder.Services.AddSingleton(_ =>
{
    var modelPath = builder.Configuration["OnnxModelPath"]
        ?? Path.Combine("..", "..", "data-pipeline", "onnx-model", "model.onnx");
    return new InferenceSession(modelPath);
});

builder.Services.AddSingleton(_ =>
{
    var tokenizerPath = builder.Configuration["TokenizerPath"]
        ?? Path.Combine("..", "..", "data-pipeline", "onnx-model", "vocab.txt");
    return BertTokenizer.Create(tokenizerPath);
});

builder.Services.AddSingleton(_ => new QdrantClient("localhost", 6334));

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();
app.UseCors("AllowFrontend");

// POST /api/search
// Accepts: { "query": "sword wielding mc" }
// Returns: top 10 semantically similar anime
app.MapPost("/api/search", async (
    SearchRequest request,
    InferenceSession onnxSession,
    BertTokenizer tokenizer,
    QdrantClient qdrant) =>
{
    if (string.IsNullOrWhiteSpace(request.Query))
        return Results.BadRequest(new { error = "Query cannot be empty." });

    // Tokenize the query
    var encoding = tokenizer.EncodeToIds(request.Query);
    int seqLen = encoding.Count;

    var inputIds = new DenseTensor<long>(new[] { 1, seqLen });
    var attentionMask = new DenseTensor<long>(new[] { 1, seqLen }); //safety measure, not really used for now

    for (int i = 0; i < seqLen; i++)
    {
        inputIds[0, i] = encoding[i];
        attentionMask[0, i] = 1;
    }

    // Run inference through the ONNX model
    var inputs = new List<NamedOnnxValue>
    {
        NamedOnnxValue.CreateFromTensor("input_ids", inputIds),
        NamedOnnxValue.CreateFromTensor("attention_mask", attentionMask),
    };

    using var results = onnxSession.Run(inputs);
    var lastHiddenState = results.First().AsTensor<float>();

    // Mean pool across the sequence dimension to get a single vector, then normalize it
    int hiddenSize = (int)lastHiddenState.Dimensions[2];
    var pooled = new float[hiddenSize];

    for (int i = 0; i < seqLen; i++)
        for (int j = 0; j < hiddenSize; j++)
            pooled[j] += lastHiddenState[0, i, j];

    for (int j = 0; j < hiddenSize; j++)
        pooled[j] /= seqLen;

    // L2 normalize so cosine similarity works correctly
    float norm = MathF.Sqrt(pooled.Sum(x => x * x));
    for (int j = 0; j < hiddenSize; j++)
        pooled[j] /= norm;

    // Query Qdrant for the top 10 closest vectors
    var searchResult = await qdrant.QueryAsync(
        collectionName: "anime",
        query: pooled,
        limit: 10
    );

    var animeResults = searchResult.Select(r => new
    {
        score = r.Score,
        title = r.Payload["title"].StringValue,
        synopsis = r.Payload["synopsis"].StringValue,
        genres = r.Payload["genres"].ListValue.Values
                  .Select(v => v.StringValue).ToList()
    });

    return Results.Ok(animeResults);
});

app.Run();

record SearchRequest(string Query);