//
//  EmptyStateView.swift
//  NuvieApp
//
//  created for phase 2. empty states
//  based on design specs
//

import SwiftUI

struct EmptyStateView: View {
    let icon: String
    let iconColor: Color
    let title: String
    let message: String
    let buttonTitle: String?
    let buttonAction: (() -> Void)?
    
    init(
        icon: String,
        iconColor: Color = Color(hex: "f59e0b"),
        title: String,
        message: String,
        buttonTitle: String? = nil,
        buttonAction: (() -> Void)? = nil
    ) {
        self.icon = icon
        self.iconColor = iconColor
        self.title = title
        self.message = message
        self.buttonTitle = buttonTitle
        self.buttonAction = buttonAction
    }
    
    var body: some View {
        VStack(spacing: 0) {
            Spacer()
            
            VStack(spacing: 16) {
                // icon
                Image(systemName: icon)
                    .font(.system(size: 64))
                    .foregroundColor(iconColor.opacity(0.2))
                
                // title
                Text(title)
                    .font(.system(size: 18, weight: .bold))
                    .foregroundColor(.white)
                    .multilineTextAlignment(.center)
                
                // message
                Text(message)
                    .font(.system(size: 14, weight: .regular))
                    .foregroundColor(Color(hex: "94a3b8"))
                    .multilineTextAlignment(.center)
                    .lineSpacing(4)
                
                // button. if provided
                if let buttonTitle = buttonTitle, let buttonAction = buttonAction {
                    Button(action: buttonAction) {
                        Text(buttonTitle)
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 44)
                            .background(
                                LinearGradient(
                                    gradient: Gradient(colors: [
                                        Color(hex: "f59e0b"),
                                        Color(hex: "d97706")
                                    ]),
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                    .padding(.top, 24)
                }
            }
            .padding(32)
            .frame(maxWidth: 280)
            
            Spacer()
        }
        .transition(.opacity)
    }
}

// MARK: - predefined empty states

struct NoRecommendationsView: View {
    let onDiscoverTap: () -> Void
    
    var body: some View {
        EmptyStateView(
            icon: "sparkles",
            iconColor: Color(hex: "f59e0b"),
            title: "No recommendations yet",
            message: "Rate some movies to get personalized recommendations",
            buttonTitle: "Discover movies",
            buttonAction: onDiscoverTap
        )
    }
}

struct NoFriendActivityView: View {
    let onFindFriendsTap: () -> Void
    
    var body: some View {
        EmptyStateView(
            icon: "person.2.fill",
            iconColor: Color(hex: "3b82f6"),
            title: "No friend activity",
            message: "Add friends to see what they're watching",
            buttonTitle: "Find friends",
            buttonAction: onFindFriendsTap
        )
    }
}

struct NoTrendingMoviesView: View {
    var body: some View {
        EmptyStateView(
            icon: "chart.line.uptrend.xyaxis",
            iconColor: Color(hex: "f97316"),
            title: "Check back later",
            message: "No trending movies available right now"
        )
    }
}

struct NoSearchResultsView: View {
    let onClearFiltersTap: (() -> Void)?
    
    var body: some View {
        EmptyStateView(
            icon: "magnifyingglass",
            iconColor: Color(hex: "94a3b8"),
            title: "No movies found",
            message: "Try different search terms or filters",
            buttonTitle: onClearFiltersTap != nil ? "Clear filters" : nil,
            buttonAction: onClearFiltersTap
        )
    }
}

struct NoWatchedMoviesView: View {
    let onDiscoverTap: () -> Void
    
    var body: some View {
        EmptyStateView(
            icon: "film",
            iconColor: Color(hex: "94a3b8"),
            title: "No watched movies",
            message: "Start watching to build your history",
            buttonTitle: "Discover movies",
            buttonAction: onDiscoverTap
        )
    }
}

struct NoRatingsView: View {
    let onRateMoviesTap: () -> Void
    
    var body: some View {
        EmptyStateView(
            icon: "star",
            iconColor: Color(hex: "fbbf24"),
            title: "No ratings yet",
            message: "Rate movies to improve your recommendations",
            buttonTitle: "Rate movies",
            buttonAction: onRateMoviesTap
        )
    }
}
