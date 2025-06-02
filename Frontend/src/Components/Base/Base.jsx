import Header from "../../Components/Header/Header";

const Base = ({ children, title, subtitle }) => {
  return (
    <>
      <div className="flex flex-row">
        <div className="w-full">
          <div className="">
            <Header title={title} subtitle={subtitle}></Header>
          </div>
          <div className="h-[calc(100%-11rem)] flex flex-col">{children}</div>
        </div>
      </div>
    </>
  );
};

export default Base;
