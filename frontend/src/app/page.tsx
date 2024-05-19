import type { NextPage } from "next";
import { Content } from "@/components/home/content";
import GanttChart from "@/gantt/GanttChart";

const Home: NextPage = () => {
  return (
    <div>
      <GanttChart/>
    </div>
  );
};
export default Home;
