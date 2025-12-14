//
//  FeedViewModel.swift
//  Nuvie
//
//  Created by Can on 14.12.2025.
//

import Foundation
import Combine

@MainActor
final class FeedViewModel: ObservableObject {

    @Published var recommendations: [Recommendation] = []
    @Published var trendingMovies: [Recommendation] = []
    @Published var activities: [Activity] = []

    @Published var isLoading: Bool = true
    @Published var showError: Bool = false
    @Published var error: AppError?
    
    init() {
        // listen for refresh notifications
        NotificationCenter.default.addObserver(
            forName: NSNotification.Name("RefreshFeed"),
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.loadFeed()
        }
    }

    func loadFeed() {
        isLoading = true
        showError = false

        Task {
            do {
                let feed = try APIClient.shared.fetchMockFeed()
                let trending = try APIClient.shared.fetchMockTrending()
                let activity = try APIClient.shared.fetchMockActivities()

                self.recommendations = feed.recommendations
                self.trendingMovies = trending.recommendations
                self.activities = activity.activities

                self.isLoading = false
                self.showError = false
                self.error = nil
            } catch {
                self.isLoading = false
                self.showError = true
                // map error to app error
                if let apiError = error as? APIError {
                    switch apiError {
                    case .fileNotFound:
                        self.error = .networkError
                    case .decoding:
                        self.error = .internalError
                    }
                } else {
                    self.error = .networkError
                }
            }
        }
    }

    func refreshFeed() async {
        loadFeed()
    }
}
