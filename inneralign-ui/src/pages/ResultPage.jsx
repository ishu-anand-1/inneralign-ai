import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import ProgressBar from "../components/ProgressBar";
import { analyzeHandwriting } from "../utils/analyzeHandwriting";
import { generatePdfReport } from "../utils/generatePdf";

const tabs = [
  { id: "features", label: "Detailed Features" },
  { id: "insights", label: "Insights & Tips" },
  { id: "handwriting", label: "Your Handwriting" },
];

const ResultPage = () => {
  const location = useLocation();
  const imagePreview = location.state?.imagePreview;
  const imageFile = location.state?.imageFile;

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [activeTab, setActiveTab] = useState("features");

  useEffect(() => {
    if (!imageFile) return;

    analyzeHandwriting(imageFile)
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [imageFile]);

  if (loading) {
    return (
      <>
        <Header />
        <main className="min-h-screen flex items-center justify-center text-xl">
          Analyzing handwriting, please wait...
        </main>
      </>
    );
  }

  return (
    <>
      <Header />

      <main className="bg-slate-50 min-h-screen py-10 px-6">
        <div className="max-w-7xl mx-auto space-y-10">

          {/* SUMMARY */}
          <section className="bg-white p-8 rounded-2xl shadow">
            <div className="flex flex-col md:flex-row justify-between gap-4">
              <div>
                <h2 className="text-3xl font-bold text-indigo-600">
                  Analysis Complete!
                </h2>

                <p className="text-gray-500">
                  Processing time: {data.processingTime} ms
                </p>

                <p className="mt-3">
                  <strong>Overall Confidence:</strong>{" "}
                  <span className="text-indigo-600 font-bold">
                    {data.overallConfidence}%
                  </span>
                </p>

                {/* CONFIDENCE MESSAGE */}
                <p className="text-sm text-indigo-600 mt-2">
                  {data.confidenceMessage}
                </p>
              </div>

              <button
                onClick={() =>
                  generatePdfReport({ ...data, imagePreview })
                }
                className="px-5 py-3 bg-black text-white rounded-xl hover:bg-gray-800"
              >
                ⬇ Download PDF Report
              </button>
            </div>
          </section>

          {/* EMOTION */}
          <section className="bg-green-500 text-white p-10 rounded-2xl shadow">
            <h3 className="text-xl font-semibold">
              Emotional State Detected
            </h3>

            <h2 className="text-4xl font-bold mt-2">
              {data.emotion}
            </h2>

            <p className="mt-2">
              Confidence: <strong>{data.emotionConfidence}%</strong>
            </p>

            <ProgressBar value={data.emotionConfidence} light />

            <ul className="mt-4 space-y-1 text-white/90">
              {data.emotionReasons.map((r, i) => (
                <li key={i}>• {r}</li>
              ))}
            </ul>
          </section>

          {/* TABBED CARD */}
          <section className="bg-white p-8 rounded-2xl shadow">

            {/* TAB BUTTONS */}
            <div className="flex gap-2 mb-8 bg-slate-100 p-1 rounded-xl w-fit">
              {tabs.map((t) => (
                <button
                  key={t.id}
                  onClick={() => setActiveTab(t.id)}
                  className={`px-5 py-2 rounded-lg text-sm font-medium transition
                    ${
                      activeTab === t.id
                        ? "bg-white shadow text-indigo-600"
                        : "text-gray-500 hover:text-black"
                    }`}
                >
                  {t.label}
                </button>
              ))}
            </div>

            {/* ---------------- TAB CONTENT ---------------- */}

            {/* DETAILED FEATURES */}
            {activeTab === "features" && (
              <div className="space-y-10">

                {/* FEATURE BARS */}
                <div>
                  <h3 className="text-xl font-semibold mb-6">
                    Handwriting Features Analysis
                  </h3>

                  {data.features.map((f, i) => (
                    <div key={i} className="mb-4">
                      <div className="flex justify-between mb-1">
                        <span>{f.name}</span>
                        <span>{f.confidence}%</span>
                      </div>
                      <ProgressBar value={f.confidence} />
                    </div>
                  ))}
                </div>

                {/* FEATURE TABLE */}
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b">
                        <th className="py-2">Feature</th>
                        <th>Value</th>
                        <th>Interpretation</th>
                        <th>Confidence</th>
                      </tr>
                    </thead>

                    <tbody>
                      {data.features.map((f, i) => (
                        <tr key={i} className="border-b last:border-none">
                          <td className="py-3 font-medium">{f.name}</td>

                          <td>{f.value}</td>

                          <td>
                            <p className="text-sm text-gray-800">
                              {f.interpretation}
                            </p>

                            {/* SIMPLE HUMAN EXPLANATION */}
                            <p className="text-sm text-gray-600 mt-1">
                              {f.simpleExplanation}
                            </p>
                          </td>

                          <td className="text-indigo-600 font-bold">
                            {f.confidence}%
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

              </div>
            )}

            {/* INSIGHTS & TIPS */}
            {activeTab === "insights" && (
              <div className="space-y-8">

                <div>
                  <h3 className="text-xl font-semibold mb-4">
                    Key Insights
                  </h3>

                  <ul className="space-y-2">
                    {data.emotionReasons.map((r, i) => (
                      <li key={i}>✓ {r}</li>
                    ))}
                  </ul>
                </div>

                {/* QUALITY FEEDBACK */}
                {data.qualitySuggestions?.length > 0 && (
                  <div>
                    <h3 className="text-xl font-semibold mb-4">
                      Image Quality Suggestions
                    </h3>

                    <ul className="space-y-2 text-gray-700">
                      {data.qualitySuggestions.map((q, i) => (
                        <li key={i}>📝 {q}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div>
                  <h3 className="text-xl font-semibold mb-4">
                    Understanding Your Results
                  </h3>

                  <p className="text-gray-600">
                    This system analyzes handwriting using computer vision and
                    machine learning. Results are probabilistic and intended
                    for educational insight, not psychological diagnosis.
                  </p>
                </div>

              </div>
            )}

            {/* YOUR HANDWRITING */}
            {activeTab === "handwriting" && (
              <div className="text-center">
                <h3 className="text-xl font-semibold mb-6">
                  Your Handwriting Sample
                </h3>

                {imagePreview ? (
                  <img
                    src={imagePreview}
                    alt="Uploaded handwriting"
                    className="mx-auto max-h-[450px] rounded-xl border"
                  />
                ) : (
                  <p className="text-gray-500">
                    No handwriting image available.
                  </p>
                )}
              </div>
            )}

          </section>

          {/* DISCLAIMER */}
          <section className="bg-blue-50 p-6 rounded-2xl text-sm shadow">
            <strong>Ethical Disclaimer:</strong> This analysis is educational
            only and does not provide medical or psychological diagnosis.
          </section>

        </div>
      </main>
    </>
  );
};

export default ResultPage;
