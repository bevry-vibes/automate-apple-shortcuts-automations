// ocr_read.swift — local OCR of an image using Apple's Vision framework
// TIER 1 (GENERIC): deterministic text reads from any screenshot, no LLM.
// Build: SDKROOT=$(xcrun --show-sdk-path) swiftc -O ocr_read.swift -o ocr
// usage: ./ocr <image-path>
//
// Why: vision LLMs misread small UI text (we watched one read "5:35" as
// "5:05" and miss an hour edit). Vision framework reads UI text with
// conf=1.00 instantly and deterministically. Coordinates are in IMAGE
// pixels — scale to native screen coordinates before clicking anything.

import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 2,
      let img = NSImage(contentsOfFile: args[1]),
      let tiff = img.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let cg = bitmap.cgImage else {
    print("usage: ocr <image>")
    exit(1)
}
let cgWidth = cg.width
let cgHeight = cg.height
let request = VNRecognizeTextRequest { req, _ in
    guard let results = req.results as? [VNRecognizedTextObservation] else { return }
    for obs in results {
        if let top = obs.topCandidates(1).first {
            let bb = obs.boundingBox
            let x = Int(bb.origin.x * CGFloat(cgWidth))
            let y = Int((1 - bb.origin.y - bb.height) * CGFloat(cgHeight))
            print("\(top.string)\t@(\(x),\(y)) conf=\(String(format: "%.2f", top.confidence))")
        }
    }
}
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try? handler.perform([request])