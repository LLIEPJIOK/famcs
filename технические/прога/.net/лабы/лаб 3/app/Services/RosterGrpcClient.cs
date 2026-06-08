using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using app.Grpc.Players;
using Google.Protobuf;
using Microsoft.Extensions.Configuration;

namespace app.Services
{
    public class RosterHttpClient
    {
        private readonly HttpClient _httpClient;
        private readonly JsonParser _jsonParser = JsonParser.Default;

        public RosterHttpClient(IConfiguration configuration)
        {
            var baseUrl = configuration["GrpcServer:Url"]?.TrimEnd('/') ?? "http://localhost:8080";
            _httpClient = new HttpClient
            {
                BaseAddress = new Uri(baseUrl)
            };
            _httpClient.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
        }

        public async Task<List<Player>> ListPlayersAsync()
        {
            var resp = await _httpClient.GetAsync("/v1/players");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            var listResp = _jsonParser.Parse<ListPlayersResponse>(json);
            return listResp.Players.ToList();
        }

        public async Task<Player> GetPlayerAsync(string playerId)
        {
            var resp = await _httpClient.GetAsync($"/v1/players/{playerId}");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return _jsonParser.Parse<Player>(json);
        }

        public async Task AddPlayerAsync(Player player)
        {
            var addReq = new AddPlayerRequest { Player = player };
            var json = JsonFormatter.Default.Format(addReq);

            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var resp = await _httpClient.PostAsync("/v1/players", content);
            resp.EnsureSuccessStatusCode();
        }

        public async Task UpdatePlayerAsync(Player player)
        {
            var updReq = new UpdatePlayerRequest { Player = player };
            var json = JsonFormatter.Default.Format(updReq);

            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var resp = await _httpClient.PutAsync($"/v1/players/{player.PlayerId}", content);
            resp.EnsureSuccessStatusCode();
        }

        public async Task DeletePlayerAsync(string playerId)
        {
            var resp = await _httpClient.DeleteAsync($"/v1/players/{playerId}");
            resp.EnsureSuccessStatusCode();
        }
    }
}
