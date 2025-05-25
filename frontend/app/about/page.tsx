import { Rss, Code, User } from "lucide-react";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div className="text-4xl">Computer Security Rankings</div>

        <br />
        <div className="text-6xl">Motivation</div>

        <div className="w-2xl">
          ComSec Rankings is a website inspired by CSrankings.org to aggregate
          publications in top tier conferences across the world. Unfortunately,
          CSrankings only accounts for labs and professors within the CS
          department of a university and calculates rankings based off that.
          <br />
          <br />
          This means that labs like SETH Lab at Texas A&M that regularly publish
          to CSS, Usenix, and S&P, but are under the ECE department, are not
          included in this ranking. ComSec Rankings ranks all universities from
          number of publications, regardless of department, straight from the
          proceedings distributed during that conference.
          <br />
          <br />
          <br />
          <div className="text-6xl">Methodology</div>
          <br />
          ComSec Rankings goes off of the digitally-accessible proceedings from
          each major conference such as this paper for the 2024 USENIX
          conference:
          <br />
          <a
            className="font-medium font-blue-200/75 underline hover:no-underline"
            href="https://www.usenix.org/sites/default/files/sec24_contents.pdf"
          >
            {" "}
            https://www.usenix.org/sites/default/files/sec24_contents.pdf{" "}
          </a>
          <br />
          <br />
          Each publication can only be counted once for a university regardless
          of how many authors are attributed to that university. If an author
          belongs to multiple universities then each university will recieve
          credit for that publication.
          <br />
          <br />
          Please note that each conference has their own timeline of how dated
          the proceedings appear which may affect the metrics displayed on the
          charts. The earliest that I have found for each conference is listed
          below:
          <br />
          <br />
          CCS: 1993
          <br />
          IEEE S&P: 2016
          <br />
          USENIX: 2015
          <br />
          <br />
          Another note for CCS is that posters listed on the proceedings are not
          counted, only papers.
          <br />
          <br />
          To find the full details of the web scraping, data processing, and
          backend API check out the source code on GitHub.
          <br />
          <br />
          <br />
          <div className="text-6xl">Meta Info</div>
          <br />
          ComSec Rankings uses Next.js and TailwindCSS on the frontend with
          Python as data collection and backend APIs. This website is hosted on
          a Hetzner VPS because Vercel could not handle the Python backend.
          <br />
          <br />
          Feel free to reach out to me at jkohhokj[at]gmail[dot]com if you have
          any comments, concerns, or questions. Alternatively, you can always
          create a pull request on this website&apos;s GitHub page.
        </div>
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
