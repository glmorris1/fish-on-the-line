import Foundation
import CoreImage

guard CommandLine.arguments.count == 2 else { exit(2) }
let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let image = CIImage(contentsOf: url),
      let detector = CIDetector(ofType: CIDetectorTypeQRCode,
                                context: CIContext(),
                                options: [CIDetectorAccuracy: CIDetectorAccuracyHigh]) else { exit(3) }
let messages = detector.features(in: image).compactMap { ($0 as? CIQRCodeFeature)?.messageString }
print(messages.joined(separator: "\n"))
exit(messages.isEmpty ? 1 : 0)
