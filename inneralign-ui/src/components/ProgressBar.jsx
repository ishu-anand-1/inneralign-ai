const ProgressBar = ({ value, label, light }) => {
  return (
    <>
      {label && (
        <p className="mb-2 text-sm font-medium text-gray-600">{label}</p>
      )}
      <div className={`w-full h-3 rounded-full ${light ? "bg-white/30" : "bg-gray-200"}`}>
        <div
          className={`h-3 rounded-full ${light ? "bg-white" : "bg-indigo-600"}`}
          style={{ width: `${value}%` }}
        />
      </div>
    </>
  );
};

export default ProgressBar;
