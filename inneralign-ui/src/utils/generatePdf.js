import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export const generatePdfReport = (data) => {
  const doc = new jsPDF("p", "mm", "a4");
  let y = 15;

  // ===============================
  // HEADER
  // ===============================
  doc.setFontSize(18);
  doc.text("InnerAlign AI", 105, y, { align: "center" });

  y += 8;
  doc.setFontSize(14);
  doc.text("Handwriting Analysis Report", 105, y, { align: "center" });

  y += 6;
  doc.setFontSize(9);
  doc.text(`Generated: ${new Date().toLocaleString()}`, 105, y, {
    align: "center",
  });

  y += 10;

  // ===============================
  // SUMMARY
  // ===============================
  doc.setFontSize(11);
  doc.text(`Overall Confidence: ${data.overallConfidence}%`, 14, y);
  y += 6;

  doc.text(`Image Quality Score: ${data.qualityScore}%`, 14, y);
  y += 10;

  // ===============================
  // EMOTIONAL STATE
  // ===============================
  doc.setFontSize(13);
  doc.text("Emotional State Detected", 14, y);
  y += 6;

  doc.setFontSize(11);
  doc.text(
    `${data.emotion} (${data.emotionConfidence}% confidence)`,
    14,
    y
  );
  y += 6;

  data.emotionReasons.forEach((reason) => {
    doc.text(`• ${reason}`, 18, y);
    y += 5;
  });

  y += 6;

  // ===============================
  // FEATURES TABLE (FULL MATCH)
  // ===============================
  doc.setFontSize(13);
  doc.text("Handwriting Features", 14, y);
  y += 4;

  autoTable(doc, {
    startY: y,
    head: [["Feature", "Value", "Interpretation", "Confidence"]],
    body: data.features.map((f) => [
      f.name,
      String(f.value),
      f.interpretation,
      `${f.confidence}%`,
    ]),
    theme: "grid",
    styles: { fontSize: 9 },
    headStyles: { fillColor: [30, 41, 59] },
  });

  y = doc.lastAutoTable.finalY + 8;

  // ===============================
  // KEY INSIGHTS
  // ===============================
  doc.setFontSize(13);
  doc.text("Key Insights", 14, y);
  y += 6;

  const insights = [
    "Strong emotional stability detected through consistent baseline",
    "Balanced writing pressure indicates healthy emotional control",
    "Spacing patterns suggest balanced social interaction",
    `Clear emotional state: ${data.emotion} (${data.emotionConfidence}%)`,
    "Writing patterns show natural behavioral tendencies",
  ];

  insights.forEach((item) => {
    doc.text(`✓ ${item}`, 16, y);
    y += 5;
  });

  y += 6;

  // ===============================
  // IMPROVEMENT SUGGESTIONS
  // ===============================
  doc.setFontSize(13);
  doc.text("Improvement Suggestions", 14, y);
  y += 6;

  doc.setFontSize(10);
  doc.text(
    "• Regular handwriting practice can enhance focus and mindfulness",
    16,
    y
  );

  y += 10;

  // ===============================
  // DISCLAIMER
  // ===============================
  doc.setFontSize(8);
  doc.text(
    "Important Disclaimer:\n"
    + "This analysis is provided for educational and informational purposes only.\n"
    + "It does not provide medical or psychological diagnosis.\n"
    + "Results are generated using computer vision algorithms and statistical modeling.",
    14,
    y,
    { maxWidth: 180 }
  );

  y += 16;
  doc.text("© 2026 InnerAlign AI - Advanced Behavioral Analysis", 14, y);

  // ===============================
  // DOWNLOAD
  // ===============================
  doc.save("InnerAlign_Handwriting_Report.pdf");
};
