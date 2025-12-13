//
//  SkeletonView.swift
//  NuvieApp
//
//  created for phase 2. loading states
//  based on design specs
//

import SwiftUI

struct SkeletonView: View {
    let width: CGFloat?
    let height: CGFloat
    let cornerRadius: CGFloat
    
    init(width: CGFloat? = nil, height: CGFloat, cornerRadius: CGFloat = 8) {
        self.width = width
        self.height = height
        self.cornerRadius = cornerRadius
    }
    
    var body: some View {
        Rectangle()
            .fill(Color(hex: "1e293b"))
            .frame(width: width, height: height)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .overlay(
                ShimmerEffect()
                    .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            )
    }
}

struct ShimmerEffect: View {
    @State private var phase: CGFloat = 0
    
    var body: some View {
        LinearGradient(
            gradient: Gradient(colors: [
                Color.clear,
                Color.white.opacity(0.1),
                Color.clear
            ]),
            startPoint: .leading,
            endPoint: .trailing
        )
        .offset(x: phase)
        .onAppear {
            withAnimation(
                Animation.linear(duration: 1.5)
                    .repeatForever(autoreverses: false)
            ) {
                phase = UIScreen.main.bounds.width * 2
            }
        }
    }
}

// MARK: - movie card skeleton

struct MovieCardSkeleton: View {
    let compact: Bool
    
    init(compact: Bool = false) {
        self.compact = compact
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // poster skeleton
            SkeletonView(width: nil, height: 0, cornerRadius: 8)
                .aspectRatio(2/3, contentMode: .fit)
            
            // title area skeleton. standard cards only
            if !compact {
                VStack(alignment: .leading, spacing: 4) {
                    SkeletonView(width: nil, height: 14, cornerRadius: 4)
                        .padding(.top, 8)
                    SkeletonView(width: nil, height: 12, cornerRadius: 4)
                }
            }
        }
    }
}

// MARK: - activity card skeleton

struct ActivityCardSkeleton: View {
    var body: some View {
        HStack(spacing: 12) {
            // avatar skeleton
            SkeletonView(width: 40, height: 40, cornerRadius: 20)
            
            // text lines skeleton
            VStack(alignment: .leading, spacing: 8) {
                SkeletonView(width: 200, height: 14, cornerRadius: 4)
                SkeletonView(width: 150, height: 12, cornerRadius: 4)
                SkeletonView(width: 180, height: 12, cornerRadius: 4)
            }
            
            Spacer()
            
            // poster thumbnail skeleton
            SkeletonView(width: 64, height: 96, cornerRadius: 8)
        }
        .padding(16)
        .background(Color(hex: "1e293b"))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// MARK: - feed screen skeletons

struct FeedSkeletonView: View {
    var body: some View {
        ScrollView {
            VStack(spacing: 32) {
                // hero section skeleton
                SkeletonView(width: nil, height: 120, cornerRadius: 16)
                
                // recommended movies skeleton
                VStack(alignment: .leading, spacing: 16) {
                    SkeletonView(width: 200, height: 20, cornerRadius: 4)
                    
                    LazyVGrid(columns: [
                        GridItem(.flexible(), spacing: 16),
                        GridItem(.flexible(), spacing: 16),
                        GridItem(.flexible(), spacing: 16)
                    ], spacing: 16) {
                        ForEach(0..<6) { _ in
                            MovieCardSkeleton()
                        }
                    }
                }
                
                // trending movies skeleton
                VStack(alignment: .leading, spacing: 16) {
                    SkeletonView(width: 150, height: 20, cornerRadius: 4)
                    
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 16) {
                            ForEach(0..<6) { _ in
                                MovieCardSkeleton(compact: true)
                                    .frame(width: 100)
                            }
                        }
                    }
                }
                
                // activity cards skeleton
                VStack(alignment: .leading, spacing: 12) {
                    SkeletonView(width: 150, height: 20, cornerRadius: 4)
                    
                    ForEach(0..<3) { _ in
                        ActivityCardSkeleton()
                    }
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 24)
        }
    }
}
