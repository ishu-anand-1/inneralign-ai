import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import Header from "../components/Header";
import ProgressBar from "../components/ProgressBar";
import { generatePdfReport } from "../utils/generatePdf";

import {
  Download,
  Brain,
  Sparkles,
  Clock,
  BadgeCheck,
} from "lucide-react";

const tabs = [
  { id: "features", label: "Detailed Features" },
  { id: "insights", label: "Insights & Tips" },
  { id: "handwriting", label: "Your Handwriting" },
];

const ResultPage = () => {
  const { state } = useLocation();
  const navigate = useNavigate();

  const data = state?.analysis;
  const imagePreview = state?.imagePreview;

  const [activeTab, setActiveTab] = useState("features");

  useEffect(() => {
    if (!data) {
      navigate("/");
    }
  }, [data, navigate]);

  if (!data) return null;

  return (
    <>
      <Header />

      <main className="bg-slate-50 min-h-screen py-10 px-6">
        <div className="max-w-7xl mx-auto space-y-10">

          {/* HERO SECTION */}
          <section className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 p-10 text-white shadow-2xl">

            <div className="relative z-10 flex flex-col lg:flex-row justify-between gap-8">

              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles size={22} />
                  <span className="uppercase tracking-wider text-sm">
                    AI Analysis Report
                  </span>
                </div>

                <h1 className="text-5xl font-bold">
                  Analysis Complete
                </h1>

                <p className="mt-4 text-white/80 max-w-xl">
                  Your handwriting has been analyzed using AI-powered
                  graphology and personality assessment models.
                </p>
              </div>

              <button
                onClick={() =>
                  generatePdfReport({
                    ...data,
                    imagePreview,
                  })
                }
                className="bg-white text-black px-6 py-4 rounded-2xl font-semibold hover:scale-105 transition"
              >
                <Download className="inline mr-2" />
                Download Report
              </button>
            </div>

            <div className="grid md:grid-cols-3 gap-5 mt-10">

              <div className="bg-white/10 backdrop-blur-lg p-5 rounded-2xl">
                <BadgeCheck />
                <p className="text-sm mt-2">Confidence</p>

                <h2 className="text-3xl font-bold">
                  {data.overallConfidence}%
                </h2>
              </div>

              <div className="bg-white/10 backdrop-blur-lg p-5 rounded-2xl">
                <Brain />
                <p className="text-sm mt-2">Detected Emotion</p>

                <h2 className="text-3xl font-bold">
                  {data.emotion}
                </h2>
              </div>

              <div className="bg-white/10 backdrop-blur-lg p-5 rounded-2xl">
                <Clock />
                <p className="text-sm mt-2">Processing Time</p>

                <h2 className="text-3xl font-bold">
                  {data.processingTime} ms
                </h2>
              </div>

            </div>
          </section>

          {/* EMOTION SECTION */}
          <section className="bg-white rounded-3xl shadow-xl p-8">

            <div className="flex items-center gap-3 mb-6">
              <Brain className="text-green-500" />

              <h2 className="text-2xl font-bold">
                Emotional Analysis
              </h2>
            </div>

            <div className="grid lg:grid-cols-2 gap-10">

              <div>
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-full font-semibold">
                  ● {data.emotion}
                </div>

                <p className="mt-5">
                  Confidence Score:

                  <span className="font-bold text-indigo-600 ml-2">
                    {data.emotionConfidence}%
                  </span>
                </p>

                <div className="mt-4">
                  <ProgressBar value={data.emotionConfidence} />
                </div>
              </div>

              <div>
                <h3 className="font-semibold mb-4">
                  Key Indicators
                </h3>

                <div className="space-y-3">
                  {data.emotionReasons?.map((reason, i) => (
                    <div
                      key={i}
                      className="bg-slate-50 border p-4 rounded-xl"
                    >
                      ✓ {reason}
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </section>

          {/* TABS */}
          <section className="bg-white p-8 rounded-3xl shadow-xl">

            <div className="flex gap-2 mb-8 bg-slate-100 p-1 rounded-xl w-fit">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-5 py-2 rounded-lg text-sm font-medium transition ${
                    activeTab === tab.id
                      ? "bg-white shadow text-indigo-600"
                      : "text-gray-500 hover:text-black"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* FEATURES TAB */}
            {activeTab === "features" && (
              <div className="space-y-8">

                <h2 className="text-2xl font-bold">
                  Handwriting Features Analysis
                </h2>

                <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">

                  {data.features?.map((feature, index) => (
                    <div
                      key={index}
                      className="bg-slate-50 border rounded-3xl p-6 hover:shadow-xl transition-all"
                    >
                      <div className="flex justify-between items-center">

                        <h3 className="font-semibold text-lg">
                          {feature.name}
                        </h3>

                        <span className="text-indigo-600 font-bold">
                          {feature.confidence}%
                        </span>
                      </div>

                      <p className="text-indigo-600 mt-2 font-medium">
                        {feature.value}
                      </p>

                      <div className="mt-4">
                        <ProgressBar value={feature.confidence} />
                      </div>

                      <p className="mt-4 text-gray-700 text-sm">
                        {feature.interpretation}
                      </p>

                      <p className="mt-2 text-gray-500 text-sm">
                        {feature.simpleExplanation}
                      </p>
                    </div>
                  ))}

                </div>

                <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-3xl p-8">

                  <h2 className="text-2xl font-bold">
                    Personality Summary
                  </h2>

                  <p className="mt-4 text-white/80 leading-relaxed">
                    Based on handwriting characteristics,
                    your writing suggests indicators of
                    emotional balance, focus, consistency,
                    and confidence.

                    The dominant emotional state detected is{" "}
                    <strong>{data.emotion}</strong>.
                  </p>

                </div>

              </div>
            )}

            {/* INSIGHTS TAB */}
            {activeTab === "insights" && (
              <div className="space-y-8">

                <div>
                  <h3 className="text-2xl font-bold mb-6">
                    AI Insights
                  </h3>

                  <div className="space-y-3">
                    {data.emotionReasons?.map((reason, i) => (
                      <div
                        key={i}
                        className="bg-slate-50 border rounded-xl p-4"
                      >
                        ✓ {reason}
                      </div>
                    ))}
                  </div>
                </div>

                {data.qualitySuggestions?.length > 0 && (
                  <div>

                    <h3 className="text-xl font-semibold mb-4">
                      Image Quality Suggestions
                    </h3>

                    <div className="space-y-3">
                      {data.qualitySuggestions.map((item, i) => (
                        <div
                          key={i}
                          className="bg-yellow-50 border border-yellow-200 rounded-xl p-4"
                        >
                          📝 {item}
                        </div>
                      ))}
                    </div>

                  </div>
                )}

              </div>
            )}

            {/* HANDWRITING TAB */}
            {activeTab === "handwriting" && (
              <div className="grid lg:grid-cols-2 gap-10 items-center">

                <div>
                  <img
                    src={imagePreview}
                    alt="Handwriting"
                    className="w-full rounded-3xl shadow-xl border"
                  />
                </div>

                <div>

                  <h2 className="text-2xl font-bold mb-6">
                    AI Inspection Areas
                  </h2>

                  <div className="space-y-4">

                    <div className="bg-slate-50 p-4 rounded-xl">
                      ✓ Letter Size Analysis
                    </div>

                    <div className="bg-slate-50 p-4 rounded-xl">
                      ✓ Baseline Detection
                    </div>

                    <div className="bg-slate-50 p-4 rounded-xl">
                      ✓ Pressure Pattern
                    </div>

                    <div className="bg-slate-50 p-4 rounded-xl">
                      ✓ Slant Recognition
                    </div>

                    <div className="bg-slate-50 p-4 rounded-xl">
                      ✓ Spacing Consistency
                    </div>

                  </div>

                </div>

              </div>
            )}

          </section>

          {/* ACTION BUTTONS */}
          <section className="flex flex-wrap justify-center gap-4">

            <button
              onClick={() => navigate("/")}
              className="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700"
            >
              Analyze New Sample
            </button>

            <button
              onClick={() =>
                generatePdfReport({
                  ...data,
                  imagePreview,
                })
              }
              className="px-6 py-3 border rounded-xl hover:bg-slate-100"
            >
              Download Report
            </button>

          </section>

          {/* DISCLAIMER */}
          <section className="bg-blue-50 p-6 rounded-2xl text-sm shadow">

            <strong>Ethical Disclaimer:</strong>

            <p className="mt-2">
              This analysis is educational only and does not
              provide medical or psychological diagnosis.
            </p>

          </section>

        </div>
      </main>
    </>
  );
};

export default ResultPage;