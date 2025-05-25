import InstitutionFrequencyChart from "./InstitutionFrequencyChart";
import { Rss, Code, User } from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_BASE_URL;
export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div className="text-5xl">Computer Security Rankings</div>
        <div className="w-2xl">
          To learn more about the motivation, methodology, and meta-information in creating this
          website, check out the {" "}
          <a
            className="font-medium font-blue-200/75 underline hover:no-underline"
            href="/about"
          >
            about section
          </a>
          .
        </div>

        <InstitutionFrequencyChart
          api={`${API}/api/top/`}
          conference_name="Top 3 Conferences"
        />

        <InstitutionFrequencyChart
          api={`${API}/api/ieee_sp/`}
          conference_name="IEEE S&P"
        />
        <InstitutionFrequencyChart
          api={`${API}/api/usenix/`}
          conference_name="USENIX"
        />
        <InstitutionFrequencyChart
          api={`${API}/api/ccs/`}
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
