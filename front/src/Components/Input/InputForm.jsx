import EyesClosed from "../../assets/img/EyesClosed.svg";
import EyesOpen from "../../assets/img/EyesOpen.svg";

import React, { useState } from "react";

function InputForm({
  user,
  forLabel,
  textLabel,
  id,
  type,
  placeholder = "Digite aqui...",
  nameInput,
  valueInput,
  maxLength,
  onChange,
  width,
  height,
  classe,
}) {
  const [isEyeOpen, setIsEyeOpen] = useState(true);
  const toggleEye = () => {
    setIsEyeOpen((prevState) => !prevState);
  };

  return (
    <>
      <div className="input-form flex flex-col w-full h-[5rem] bg-[var(--color-gray)] justify-center content-start rounded-[0.5rem] my-[1.5rem] pl-[1.5rem]">
        <div className="flex flex-row justify-start content-center gap-2">
          <i className="flex">
            <img src={user} />
          </i>
          <label
            htmlFor={forLabel}
            className="flex text-[1.25rem] font-[var(--font-primary)] font-medium text-[var(--color-gray-2)]"
          >
            {textLabel}
          </label>
        </div>
        <div className="flex ">
          <input
            id={id}
            type={
              type === "password" ? (isEyeOpen ? "password" : "text") : type
            }
            placeholder={placeholder}
            name={nameInput}
            value={valueInput}
            maxLength={maxLength}
            accept="Digits"
            onChange={onChange}
            className={`${width} ${height} text-[1.5rem] text-[var(--black)] font-[var(--font-primary)] font-medium flex-wrap rounded-[0.5rem] outline-none bg-[var(--color-gray)]`}
            required
          />
          <button
            type="button"
            className={`${classe} flex mr-4`}
            onClick={toggleEye}
          >
            <img
              className="text-[var(--black)]"
              src={isEyeOpen ? EyesOpen : EyesClosed}
              alt="Toggle Eye"
            />
          </button>
        </div>
      </div>
    </>
  );
}

export default InputForm;
