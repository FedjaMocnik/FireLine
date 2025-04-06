import React from "react";

const ImageCard = ({ imageSrc, title, description }) => {
  return (
    <div className="max-w-sm mx-auto bg-white rounded-2xl shadow-md overflow-hidden text-center">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">{title}</h2>
        <div className="flex justify-center">
          <img
            src={imageSrc}
            alt={title}
            className="w-full h-64 object-cover rounded-lg"
          />
        </div>
        <p className="mt-4 text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
};


export default ImageCard;