export const analyzeHandwriting = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        overallConfidence: 91.1,
        emotion: "Happy / Positive",
        emotionConfidence: 95,
        qualityScore: 92,
        features: [
          { name: "Slant Angle", value: "14.7°", confidence: 94, tag: "Excellent" },
          { name: "Baseline Consistency", value: "0.91", confidence: 98, tag: "Excellent" },
          { name: "Stroke Pressure", value: "0.88", confidence: 87, tag: "Good" },
          { name: "Letter Spacing", value: "1.27", confidence: 98, tag: "Excellent" },
          { name: "Word Spacing", value: "2.25", confidence: 93, tag: "Excellent" },
          { name: "X-Height Variation", value: "0.33", confidence: 83, tag: "Good" },
          { name: "Loop Openness", value: "0.95", confidence: 80, tag: "Good" },
          { name: "Writing Speed Proxy", value: "0.76", confidence: 79, tag: "Good" },
        ],
      });
    }, 2000);
  });
};
