import React from "react";
import { useState, useEffect } from "react";

function Select({ name, selectName, onSelectionChange }) {
  const [selectedValue, setSelectedValue] = useState("0");
  const [click, setClick] = useState(false);

  const handleClick = () => {
    setClick(!click);
  };

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedValue(value);
    if (onSelectionChange) {
      onSelectionChange(value);
    }
  };

  return (
    <>
      <div className="relative">
        <select
          value={selectedValue}
          onChange={handleChange}
          className="appearance-none w-[18vw] h-[4.6rem] rounded-[2.7rem] font-semibold text-[1.6rem] flex justify-center items-center pl-5 bg-white text-quinary outline-primary transition duration-700 ease-in-out shadow-xl"
          onClick={handleClick}
        >
          <option className="" value="0">
            {name}
          </option>
          {selectName.map((item) => (
            <option key={item.id} value={item.id}>
              {item.cd_categoria || item.descricao}
            </option>
          ))}
        </select>
        <span className="pointer-events-none col-start-1 row-start-1 absolute left-[calc(15.5vw)] top-[2.4rem] -translate-y-1/2 text-quinary dark:text-quinary material-icons">
          {click ? "keyboard_arrow_right" : "keyboard_arrow_down"}
        </span>
      </div>
    </>
  );
}

export default Select;
