function Btn({
  id,
  nameBtn,
  width,
  height,
  name,
  onClick,
  disabled = false,
  color,
  hover,
  outline,
  active,
  className,
}) {
  return (
    <button
      id={id}
      type="submit"
      name={name}
      onClick={onClick}
      className={`${width} ${height} ${className}
        font-[var(--font-primary)]
        cursor-pointer
        text-[1.25rem] text-white
        font-medium flex-wrap
        bg-${color}
        border border-none rounded-[1rem]
        flex justify-center items-center
        hover:bg-${hover}
        focus:outline-2 focus:outline-offset-2
        focus:outline-${outline}
        active:bg-${active}
        transition duration-700 ease-in-out`}
      disabled={disabled}
    >
      {nameBtn}
    </button>
  );
}

export default Btn;
