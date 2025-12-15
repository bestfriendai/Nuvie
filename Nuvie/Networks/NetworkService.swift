//
//  NetworkService.swift
//  Nuvie
//
//  Created by Can on 15.12.2025.
//

import Foundation

enum NetworkError: Error {
    case badURL
    case badResponse
    case http(Int)
    case decode
}

final class NetworkService {
    static let shared = NetworkService()
    private init() {}

    func get<T: Decodable>(_ path: String, as: T.Type) async throws -> T {
        let full = APIClient.shared.baseURL + path
        guard let url = URL(string: full) else { throw NetworkError.badURL }

        var req = URLRequest(url: url)
        req.httpMethod = "GET"

        for (k,v) in APIClient.shared.defaultHeaders {
            req.setValue(v, forHTTPHeaderField: k)
        }

        let (data, res) = try await URLSession.shared.data(for: req)
        guard let http = res as? HTTPURLResponse else { throw NetworkError.badResponse }
        guard (200...299).contains(http.statusCode) else { throw NetworkError.http(http.statusCode) }

        do { return try JSONDecoder().decode(T.self, from: data) }
        catch { throw NetworkError.decode }
    }
}
