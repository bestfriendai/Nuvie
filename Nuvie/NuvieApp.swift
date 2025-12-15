//
//  NuvieApp.swift
//  Nuvie
//
//  Created by Can on 14.12.2025.
//

import SwiftUI

@main
struct NuvieApp: App {
    @StateObject private var feedViewModel = FeedViewModel()
    init() {
            
            UserDefaults.standard.set("503275072513d5e4766ffe7caa7300a7", forKey: "api_key")
        }
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(feedViewModel)
        }
    }
}
