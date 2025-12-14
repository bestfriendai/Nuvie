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
            } catch {
                self.isLoading = false
                self.showError = true
            }
        }
    }

    func refreshFeed() async {
        loadFeed()
    }
}
