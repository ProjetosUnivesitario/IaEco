import Btn from "../../Components/Button/Btn";
import { signOut } from "../../hooks/Auth";
import { transformRequest } from "../../utils/transformRequest";
import { useState, useEffect } from "react";
import Logomarca from "../../assets/img/Logomarca.png";

function Header({ title, subtitle }) {
  const [name, setName] = useState("");

  useEffect(() => {
    async function handleChange() {
      const token = localStorage.getItem("access");
      const data = await transformRequest(
        "/api/v1/user/me",
        "GET",
        null,
        token
      );
      setName(data);
    }
    handleChange();
  }, []);

  const handleLogout = () => {
    signOut();
  };

  return (
    <div className="w-full px-4 py-6 md:py-10 flex flex-col md:flex-row items-center justify-between gap-6 md:gap-0">
      <img
        src={Logomarca}
        alt="Logomarca"
        className="w-40 md:w-60"
      />

      <div className="text-center md:text-left">
        <h1 className="text-2xl md:text-4xl font-bold text-quaternary font-[var(--font-primary)]">
          {title}
        </h1>
        <h2 className="text-lg md:text-2xl font-semibold text-quinary font-[var(--font-primary)]">
          {subtitle}
        </h2>
      </div>

      <div className="flex flex-col md:flex-row items-center gap-3 md:gap-5">
        <h1 className="text-lg md:text-2xl text-quinary font-semibold font-[var(--font-primary)]">
          {name?.first_name} {name?.last_name}
        </h1>
        <Btn
          id="Logout"
          nameBtn="Sair"
          width="w-[6rem] md:w-[7rem]"
          height="h-[3.2rem] md:h-[3.8rem]"
          className="bg-danger hover:bg-danger-hover focus:outline-danger-hover active:bg-danger-hover"
          onClick={handleLogout}
        />
      </div>
    </div>
  );
}

export default Header;
