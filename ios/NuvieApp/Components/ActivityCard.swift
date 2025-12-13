//
//  ActivityCard.swift
//  NuvieApp
//
//  created for phase 2. feed screen design
//  based on react component reference and design specs
//

import SwiftUI

struct ActivityCard: View {
    let activity: Activity
    
    var body: some View {
        HStack(spacing: 12) {
            // friend avatar
            AsyncImage(url: URL(string: activity.user_avatar ?? "")) { phase in
                switch phase {
                case .empty:
                    AvatarPlaceholder()
                case .success(let image):
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                case .failure:
                    AvatarPlaceholder()
                @unknown default:
                    AvatarPlaceholder()
                }
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())
            
            // activity content
            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 6) {
                    Text(activity.user_name)
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(.white)
                    
                    activityIcon
                    
                    Text(activityText)
                        .font(.system(size: 14))
                        .foregroundColor(Color(hex: "94a3b8"))
                }
                
                Text(activity.formattedDate)
                    .font(.system(size: 12))
                    .foregroundColor(Color(hex: "64748b"))
                
                // rating stars. if rating activity
                if activity.type == .rating, let rating = activity.rating {
                    HStack(spacing: 2) {
                        ForEach(0..<5) { index in
                            Image(systemName: index < rating ? "star.fill" : "star")
                                .font(.system(size: 12))
                                .foregroundColor(index < rating ? Color(hex: "fbbf24") : Color(hex: "475569"))
                        }
                    }
                    .padding(.top, 4)
                }
                
                // comment. if review activity
                if let comment = activity.comment, !comment.isEmpty {
                    Text(comment)
                        .font(.system(size: 14))
                        .foregroundColor(Color(hex: "cbd5e1"))
                        .lineLimit(2)
                        .padding(.top, 4)
                }
            }
            
            Spacer()
            
            // movie poster thumbnail
            AsyncImage(url: URL(string: activity.movie_poster ?? "")) { phase in
                switch phase {
                case .empty:
                    PosterThumbnailPlaceholder()
                case .success(let image):
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                case .failure:
                    PosterThumbnailPlaceholder()
                @unknown default:
                    PosterThumbnailPlaceholder()
                }
            }
            .frame(width: 64, height: 96)
            .clipShape(RoundedRectangle(cornerRadius: 8))
        }
        .padding(16)
        .background(Color(hex: "1e293b").opacity(0.5))
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color(hex: "334155").opacity(0.5), lineWidth: 1)
        )
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
    
    private var activityIcon: some View {
        Group {
            switch activity.type {
            case .rating:
                Image(systemName: "star.fill")
                    .font(.system(size: 12))
                    .foregroundColor(Color(hex: "fbbf24"))
            case .review:
                Image(systemName: "message.fill")
                    .font(.system(size: 12))
                    .foregroundColor(Color(hex: "3b82f6"))
            case .watchlist:
                Image(systemName: "bookmark.fill")
                    .font(.system(size: 12))
                    .foregroundColor(Color(hex: "a855f7"))
            case .watched, .started:
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 12))
                    .foregroundColor(Color(hex: "10b981"))
            }
        }
    }
    
    private var activityText: String {
        switch activity.type {
        case .rating:
            return "rated \(activity.movie_title)"
        case .review:
            return "reviewed \(activity.movie_title)"
        case .watchlist:
            return "added \(activity.movie_title) to watchlist"
        case .watched:
            return "watched \(activity.movie_title)"
        case .started:
            return "started watching \(activity.movie_title)"
        }
    }
}

struct AvatarPlaceholder: View {
    var body: some View {
        Circle()
            .fill(Color(hex: "334155"))
            .overlay(
                Image(systemName: "person.fill")
                    .font(.system(size: 20))
                    .foregroundColor(Color(hex: "64748b"))
            )
    }
}

struct PosterThumbnailPlaceholder: View {
    var body: some View {
        RoundedRectangle(cornerRadius: 8)
            .fill(Color(hex: "334155"))
            .overlay(
                Image(systemName: "film")
                    .font(.system(size: 24))
                    .foregroundColor(Color(hex: "64748b"))
            )
    }
}
