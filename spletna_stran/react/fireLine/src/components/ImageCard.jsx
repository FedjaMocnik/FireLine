import React from "react";

const ImageCard = ({ imageSrc, title, description }) => {
  return (
    <div className="mx-auto bg-white rounded-2xl shadow-md overflow-hidden text-center w-full max-w-[600px]">
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
        <div className="flex justify-center">
          <img
            src={imageSrc}
            alt={title}
            style={{ width: "400px" }}
            className="object-cover rounded-lg"
          />
        </div>
        <p className="mt-4 text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
};

export default ImageCard;
