import HeroSearch from "../components/HeroSearch";

function Home(props) {
  const repeatSearch = (item) => {
    if (item.type === "text") {
      props.setActiveTab("text");
      props.setTextQuery(item.label);
      props.handleSearch({ type: "text", query: item.label });
    }
  };

  return (
    <main>
      <HeroSearch {...props} />
    </main>
  );
}

export default Home;
