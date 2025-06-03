import Logo from "../../assets/img/Logomarca.png";

function Error() {
  return (
    <>
      <div className="h-[100vh] flex flex-col gap-2 items-center justify-center">
        <p className="text-quaternary font-[var(--font-primary)] font-bold text-[5rem]">
          ACESSO NEGADO
        </p>
        <p className="text-quaternary font-[var(--font-primary)] font-bold text-[5rem] mb-[6rem]">
          CÓDIGO DO ERRO: 403
        </p>
        <img src={Logo} className="w-[30rem]" />
      </div>
    </>
  );
}

export default Error;
