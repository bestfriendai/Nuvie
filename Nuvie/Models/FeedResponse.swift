//
//  FeedResponse.swift
//  Nuvie
//
//  Created by Can on 14.12.2025.
//

import Foundation

struct FeedResponse: Codable {
    let recommendations: [Recommendation]
    let last_updated: String
    let total_count: Int
}
