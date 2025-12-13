//
//  Activity.swift
//  NuvieApp
//
//  placeholder. temporary model for ui development
//  todo: teammate should implement final models with proper decoding
//
//  created for phase 2. ui components need these to compile
//  based on api contracts from /docs/api_contracts.md
//

import Foundation

struct Activity: Codable, Identifiable {
    let activity_id: Int
    let user_id: Int
    let user_name: String
    let user_avatar: String?
    let movie_id: Int
    let movie_title: String
    let movie_poster: String?
    let type: ActivityType
    let rating: Int?
    let comment: String?
    let timestamp: String
    
    var id: Int { activity_id }
    
    var formattedDate: String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: timestamp) else {
            return timestamp
        }
        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .medium
        displayFormatter.timeStyle = .none
        return displayFormatter.string(from: date)
    }
}

enum ActivityType: String, Codable {
    case rating
    case review
    case watched
    case started
    case watchlist
}

struct ActivityFeedResponse: Codable {
    let activities: [Activity]
    let total_count: Int
}
