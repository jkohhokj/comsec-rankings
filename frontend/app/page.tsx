import InstitutionFrequencyChart from "./InstitutionFrequencyChart";
import { Rss, Code, User } from "lucide-react";
export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div className="text-5xl">Computer Security Rankings</div>
        <div className="w-2xl">
          ComSec Rankings is a website inspired by CSrankings.org to aggregate
          publications in top tier conferences across the world. Unfortunately,
          CSrankings only accounts for labs and professors within the CS
          department of a university so labs like SETH Lab at Texas A&M that
          regularly publish to CSS, Usenix, and S&P, but are under the ECE
          department, are not included in this list. ComSec Rankings ranks all
          universities from number of publications, regardless of department
          together.
        </div>

        <InstitutionFrequencyChart
          api="http://localhost:8003/"
          conference_name="Top 3 Conferences"
        />

        <InstitutionFrequencyChart
          api="http://localhost:8000/"
          conference_name="IEEE S&P"
        />
        <InstitutionFrequencyChart
          api="http://localhost:8001/"
          conference_name="USENIX"
        />
        <InstitutionFrequencyChart
          api="http://localhost:8002/"
          conference_name="ACM CCS"
        />
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href={"https://www.jkoh.dev"}
          target="_blank"
          rel="noopener noreferrer"
        >
          <User color="white" size={36} />
          About Me
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href={"https://github.com/jkohhokj/comsec-rankings"}
          target="_blank"
          rel="noopener noreferrer"
        >
          <Code color="white" size={36} />
          Source Code
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href={"https://blog.jkoh.dev/"}
          target="_blank"
          rel="noopener noreferrer"
        >
          <Rss color="white" size={36} />
          Blog
        </a>
      </footer>
    </div>
  );
}
