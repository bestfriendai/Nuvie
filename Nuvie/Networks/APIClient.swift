//
//  APIClient.swift
//  Nuvie
//
//  Created by Can on 14.12.2025.
//

import Foundation

enum APIError: Error {
    case fileNotFound(String)
    case decoding
}

final class APIClient {

    static let shared = APIClient()
    private init() {}

    // MARK: - Tokens
    private var authToken: String? {
        // Keep it simple
        TokenStore.shared.load()
    }

    private let internalToken = "INTERNAL_AI_TOKEN"

    // MARK: - Headers
    var defaultHeaders: [String: String] {
        var headers: [String: String] = [
            "Content-Type": "application/json",
            "X-Internal-Token": internalToken
        ]

        if let token = authToken {
            headers["Authorization"] = "Bearer \(token)"
        }
        if let apiKey = UserDefaults.standard.string(forKey: "api_key") {
            headers["x-api-key"] = apiKey
        }

        return headers
    }
}
extension APIClient {

    private func loadJSON<T: Decodable>(_ filename: String, as type: T.Type) throws -> T {
        guard let url = Bundle.main.url(forResource: filename, withExtension: "json") else {
            throw APIError.fileNotFound(filename)
        }

        let data = try Data(contentsOf: url)

        do {
            return try JSONDecoder().decode(T.self, from: data)
        } catch {
            throw APIError.decoding
        }
    }

    // MARK: - Mock fetchers (Phase 2)

    func fetchMockFeed() throws -> FeedResponse {
        try loadJSON("mock_feed", as: FeedResponse.self)
    }

    func fetchMockTrending() throws -> FeedResponse {
        try loadJSON("mock_trending", as: FeedResponse.self)
    }

    func fetchMockActivities() throws -> ActivityFeedResponse {
        try loadJSON("mock_activities", as: ActivityFeedResponse.self)
    }
}

enum APIEnvironment {
    case dev
    case prod
}

extension APIClient {

    var environment: APIEnvironment {
        return .dev
    }

    var baseURL: String {
        switch environment {
        case .dev:
            return "https://api.dev.nuvie.com"
        case .prod:
            return "https://api.nuvie.com"
        }
    }
}
extension APIClient {

    // GET request (live API)
    func get<T: Decodable>(
        endpoint: Endpoint,
        responseType: T.Type
    ) async throws -> T {

        let url = endpoint.url(baseURL: baseURL)

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        defaultHeaders.forEach {
            request.setValue($0.value, forHTTPHeaderField: $0.key)
        }

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw URLError(.badServerResponse)
        }

        return try JSONDecoder().decode(T.self, from: data)
    }

    // POST request (rate movie etc.)
    func post<T: Decodable, Body: Encodable>(
        endpoint: Endpoint,
        body: Body,
        responseType: T.Type
    ) async throws -> T {

        let url = endpoint.url(baseURL: baseURL)

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = try JSONEncoder().encode(body)

        defaultHeaders.forEach {
            request.setValue($0.value, forHTTPHeaderField: $0.key)
        }

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw URLError(.badServerResponse)
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}

