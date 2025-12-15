//
//  ExplanationBadges.swift
//  Nuvie
//
//  Created by Can on 15.12.2025.
//

import Foundation

import SwiftUI

struct ExplanationBadge: View {
    let explanation: Explanation
    @Binding var showSheet: Bool
    
    init(explanation: Explanation, showSheet: Binding<Bool> = .constant(false)) {
        self.explanation = explanation
        self._showSheet = showSheet
    }
    
    var body: some View {
        Button(action: {
            showSheet = true
        }) {
            HStack(spacing: 4) {
                Image(systemName: iconName)
                    .font(.system(size: 11))
                Text(primaryReasonText)
                    .font(.system(size: 11, weight: .medium))
            }
            .foregroundColor(iconColor)
            .padding(.horizontal, 6)
            .padding(.vertical, 4)
            .background(iconColor.opacity(0.2))
            .clipShape(RoundedRectangle(cornerRadius: 4))
        }
    }
    
    private var iconName: String {
        switch explanation.primary_reason {
        case "genre_match":
            return "sparkles"
        case "friend_activity":
            return "person.2.fill"
        case "similar_movies":
            return "film.fill"
        case "popular":
            return "chart.bar.fill"
        default:
            return "questionmark.circle.fill"
        }
    }
    
    private var iconColor: Color {
        switch explanation.primary_reason {
        case "genre_match":
            return Color(hex: "f59e0b")
        case "friend_activity":
            return Color(hex: "3b82f6")
        case "similar_movies":
            return Color(hex: "10b981")
        case "popular":
            return Color(hex: "f97316")
        default:
            return Color(hex: "94a3b8")
        }
    }
    
    private var primaryReasonText: String {
        if let topFactor = explanation.factors.first {
            return topFactor.description
        }
        
        switch explanation.primary_reason {
        case "genre_match":
            return "matches your taste"
        case "friend_activity":
            if let friendRatings = explanation.factors.first(where: { $0.type == "friend_activity" })?.payload?["count"] {
                return "\(friendRatings) friends loved this"
            }
            return "friends recommend"
        case "similar_movies":
            return "similar to your favorites"
        case "popular":
            return "trending now"
        default:
            return "recommended for you"
        }
    }
}

struct ExplanationSheet: View {
    let explanation: Explanation
    let movieTitle: String
    @Binding var isPresented: Bool
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    // header
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Why this movie?")
                            .font(.system(size: 24, weight: .bold))
                            .foregroundColor(.white)
                        
                        Text(movieTitle)
                            .font(.system(size: 18, weight: .medium))
                            .foregroundColor(Color(hex: "94a3b8"))
                    }
                    .padding(.bottom, 8)
                    
                    // confidence badge
                    HStack {
                        Text("Confidence: \(Int(explanation.confidence * 100))%")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(.white)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Color(hex: "f59e0b").opacity(0.2))
                            .clipShape(Capsule())
                    }
                    
                    // factors
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Reasons")
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(.white)
                        
                        ForEach(Array(explanation.factors.enumerated()), id: \.offset) { index, factor in
                            ExplanationFactorCard(factor: factor, index: index + 1)
                        }
                    }
                }
                .padding(24)
            }
            .background(Color(hex: "0f172a"))
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        isPresented = false
                    }
                    .foregroundColor(Color(hex: "f59e0b"))
                }
            }
        }
    }
}

struct ExplanationFactorCard: View {
    let factor: ExplanationFactor
    let index: Int
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // number badge
            Text("\(index)")
                .font(.system(size: 14, weight: .bold))
                .foregroundColor(.white)
                .frame(width: 28, height: 28)
                .background(factorColor.opacity(0.3))
                .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 4) {
                // type label
                Text(factorTypeLabel)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(factorColor)
                
                // description
                Text(factor.description)
                    .font(.system(size: 14))
                    .foregroundColor(.white)
                    .fixedSize(horizontal: false, vertical: true)
                
                // weight indicator
                HStack(spacing: 4) {
                    Text("Weight: \(Int(factor.weight * 100))%")
                        .font(.system(size: 11))
                        .foregroundColor(Color(hex: "94a3b8"))
                }
                .padding(.top, 4)
            }
            
            Spacer()
        }
        .padding(16)
        .background(Color(hex: "1e293b"))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
    
    private var factorTypeLabel: String {
        switch factor.type {
        case "genre_match":
            return "Genre Match"
        case "friend_activity":
            return "Friend Activity"
        case "similar_movies":
            return "Similar Movies"
        case "popular":
            return "Popular"
        default:
            return factor.type.capitalized
        }
    }
    
    private var factorColor: Color {
        switch factor.type {
        case "genre_match":
            return Color(hex: "f59e0b")
        case "friend_activity":
            return Color(hex: "3b82f6")
        case "similar_movies":
            return Color(hex: "10b981")
        case "popular":
            return Color(hex: "f97316")
        default:
            return Color(hex: "94a3b8")
        }
    }
}


