import { useNavigate } from "react-router-dom";
import { Upload, Brain, BarChart3, Zap, CheckCircle } from "lucide-react";
import Header from "../components/Header";
import UploadCard from "../components/UploadCard";
import { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { analyzeHandwriting } from "../utils/analyzeHandwriting";

const UploadPage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  /* ---------------- FILE SELECT ---------------- */
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!["image/png", "image/jpeg"].includes(file.type)) {
      alert("Only JPG or PNG images allowed");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert("Max file size is 10MB");
      return;
    }

    setSelectedFile(file);

    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(file);
  };

  /* ---------------- ANALYZE ---------------- */
const handleAnalyze = async () => {
  if (!selectedFile) return;

  setAnalyzing(true);

  try {
    const result = await analyzeHandwriting(selectedFile);

    navigate("/result", {
      state: {
        imagePreview: preview,
        analysis: result, // ✅ ML response
      },
    });

  } catch (error) {
    console.error(error);
    alert("Analysis failed. Please try again.");
    setAnalyzing(false);
  }
};



  return (
    <>
      <Header />

      <main className="max-w-7xl mx-auto px-6 py-14">
        {/* HERO */}
        <section className="text-center max-w-4xl mx-auto">
          <h2 className="text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-500 bg-clip-text text-transparent">
            Discover Your Inner Self Through Writing
          </h2>
          <p className="mt-5 text-lg text-gray-600">
            Advanced AI-powered handwriting analysis using ML & Computer Vision
          </p>
        </section>

        {/* FEATURES */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <UploadCard icon={<Brain />} title="Advanced ML Analysis"
            description="Two-stage neural network for feature extraction" />
          <UploadCard icon={<BarChart3 />} title="Emotion Detection"
            description="Behavioral inference from handwriting traits" />
          <UploadCard icon={<Zap />} title="Explainable AI"
            description="Clear insights with confidence scores" />
        </section>

        {/* UPLOAD / ANALYZE CARD */}
        <section className="mt-20">
          <motion.div
            layout
            className="border-2 border-dashed border-gray-300 rounded-3xl bg-white p-14 text-center max-w-4xl mx-auto shadow-sm cursor-pointer"
            onClick={() => !analyzing && fileInputRef.current.click()}
          >

            <AnimatePresence mode="wait">

              {/* ---------------- DEFAULT / READY ---------------- */}
              {!analyzing && (
                <motion.div
                  key="upload"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >

                  <div className="w-20 h-20 rounded-full bg-gradient-to-br from-indigo-600 to-purple-500 flex items-center justify-center mx-auto mb-6">
                    {selectedFile ? (
                      <CheckCircle className="text-white w-8 h-8" />
                    ) : (
                      <Upload className="text-white w-8 h-8" />
                    )}
                  </div>

                  <h3 className="text-2xl font-semibold mb-2">
                    {selectedFile ? "Ready to Analyze" : "Upload Your Handwriting"}
                  </h3>

                  <p className="text-gray-600 mb-6">
                    {selectedFile
                      ? selectedFile.name
                      : "Drag & drop or click anywhere to upload"}
                  </p>

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/png, image/jpeg"
                    onChange={handleFileChange}
                    className="hidden"
                  />

                  {selectedFile && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAnalyze();
                      }}
                      className="bg-black text-white px-10 py-3 rounded-xl hover:bg-gray-800 transition"
                    >
                      Analyze Handwriting
                    </button>
                  )}

                  <div className="flex justify-center gap-6 mt-6 text-sm text-gray-500">
                    <span>✔ JPG / PNG</span>
                    <span>✔ Max 10MB</span>
                    <span>✔ 2–3 lines optimal</span>
                  </div>

                </motion.div>
              )}

              {/* ---------------- ANALYZING UI (SCREENSHOT MATCH) ---------------- */}
              {analyzing && (
                <motion.div
                  key="analyzing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className="w-20 h-20 rounded-full border-4 border-indigo-500 border-t-transparent animate-spin mx-auto mb-6" />

                  <h3 className="text-2xl font-semibold mb-2">
                    Analyzing Your Handwriting...
                  </h3>

                  <p className="text-gray-500 mb-8">
                    Running advanced ML pipeline — this may take a few seconds
                  </p>

                  <div className="space-y-3 text-left max-w-md mx-auto text-gray-600">
                    <p>✔ Image preprocessing & quality check</p>
                    <p>✔ Extracting handwriting features (CV)</p>
                    <p>✔ Running emotion detection model</p>
                    <p>✔ Generating insights & confidence scores</p>
                  </div>
                </motion.div>
              )}

            </AnimatePresence>
          </motion.div>
        </section>
      </main>
    </>
  );
};

export default UploadPage;
