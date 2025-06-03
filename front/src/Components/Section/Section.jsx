import { Link } from "react-router-dom";

function Section({ Icon, Text, link }) {
  return (
    <>
      <Link to={link}>
        <div className="w-[21.4rem] h-[4.4rem] rounded-[2rem] bg-[var(--white)] flex justify-between items-center p-[2rem] transition duration-700 ease-in-out hover:bg-secondary">
          <div className="w-[24px] h-[24px] bg-[var(--color-primary)] rounded-[0.4rem] flex justify-center items-center">
            <span
              className="material-icons"
              style={{ fontSize: "18px", color: "#fff" }}
            >
              {Icon}
            </span>
          </div>
          <div className="w-[115px] h-auto overflow-hidden">
            <p className="text-[var(--color-gray-3)] font-bold text-[1.3rem] text-left whitespace-wrap text-ellipsis">
              {Text}
            </p>
          </div>
        </div>
      </Link>
    </>
  );
}

export default Section;
