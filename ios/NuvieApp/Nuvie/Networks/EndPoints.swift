//
//  EndPoints.swift
//  Nuvie
//
//  Created by Can on 14.12.2025.
//

import Foundation

enum Endpoint {

    case feedRecommendations
    case movie(id: String)
    case rateMovie(id: String)
    case activityFeed

    var path: String {
        switch self {
        case .feedRecommendations:
            return "/feed/recommendations"

        case .movie(let id):
            return "/movies/\(id)"

        case .rateMovie(let id):
            return "/movies/\(id)/rate"

        case .activityFeed:
            return "/feed/activities"
        }
    }
}
