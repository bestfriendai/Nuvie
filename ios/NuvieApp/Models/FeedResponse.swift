//
//  FeedResponse.swift
//  NuvieApp
//
//  placeholder. temporary model for ui development
//  todo: teammate should implement final models with proper decoding
//
//  created for phase 2. ui components need these to compile
//  based on api contracts from /docs/api_contracts.md
//

import Foundation

struct FeedResponse: Codable {
    let recommendations: [Recommendation]
    let last_updated: String
    let total_count: Int
}
