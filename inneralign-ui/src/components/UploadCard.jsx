import React from "react";

const UploadCard = ({ icon, title, description }) => {
  return (
    <div className="
      bg-white
      rounded-2xl
      p-6
      shadow-md
      hover:shadow-xl
      transition-all
      duration-300
      hover:-translate-y-1
      flex
      flex-col
      gap-4
    ">
      {/* ICON */}
      <div className="
        w-12 h-12
        rounded-xl
        bg-gradient-to-br from-indigo-100 to-purple-100
        flex items-center justify-center
        text-indigo-600
        text-xl
      ">
        {icon}
      </div>

      {/* TITLE */}
      <h3 className="text-lg font-semibold text-gray-900">
        {title}
      </h3>

      {/* DESCRIPTION */}
      <p className="text-sm text-gray-600 leading-relaxed">
        {description}
      </p>
    </div>
  );
};

export default UploadCard;
