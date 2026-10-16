import { useState, useEffect } from "react";
import heroPhoto from "@/imports/Screenshot_2026-07-27_at_2.13.24_PM.png";
import trackerPhoto from "@/imports/DSCN1352.jpeg";
import tetPeakPhoto from "@/imports/tet_peak.jpg";
import mountDrewPhoto from "@/imports/mount_drew.jpg";
import mtTantalusPhoto from "@/imports/mt_tantalus.jpeg";
import mountChurchillPhoto from "@/imports/mount_churchill.jpg";
import penguinArt from "@/imports/Untitled_Artwork.png";

const NAV_LINKS = [
  { label: "Home" },
  { label: "Ezra Tracker" },
  { label: "Future Dreams" },
  { label: "Quotes" },
  { label: "Socials" },
];

const FACTS: { label: string; value: string; note?: string; href?: string }[] = [
  { label: "Favorite ice cream", value: "The Tonight Dough", note: "Ben & Jerry's", href: "https://www.benjerry.com/flavors/the-tonight-dough-ice-cream" },
  { label: "All-time favorite color", value: "Tourquise" },
  { label: "Second biggest fear", value: "Darkness" },
];

const LEGEND = [
  { color: "bg-blue-500", label: "Travel Plans" },
  { color: "bg-red-500", label: "Hikes" },
  { color: "bg-green-500", label: "Sidequests" },
];

function Nav({
  activeNav,
  setActiveNav,
  menuOpen,
  setMenuOpen,
}: {
  activeNav: string;
  setActiveNav: (v: string) => void;
  menuOpen: boolean;
  setMenuOpen: (v: boolean | ((o: boolean) => boolean)) => void;
}) {
  return (
    <nav className="relative z-10">
      <div className="flex items-center justify-between px-5 py-8">
        <button
          className="md:hidden p-2 text-white/60 hover:text-white transition-colors"
          onClick={() => setMenuOpen((o) => !o)}
          aria-label="Toggle menu"
        >
          <div className={`w-5 h-0.5 bg-current mb-1 transition-all duration-200 ${menuOpen ? "rotate-45 translate-y-1.5" : ""}`} />
          <div className={`w-5 h-0.5 bg-current mb-1 transition-all duration-200 ${menuOpen ? "opacity-0" : ""}`} />
          <div className={`w-5 h-0.5 bg-current transition-all duration-200 ${menuOpen ? "-rotate-45 -translate-y-1.5" : ""}`} />
        </button>
        <ul className="hidden md:flex gap-6">
          {NAV_LINKS.map((link) => (
            <li key={link.label}>
              <button
                onClick={() => setActiveNav(link.label)}
                className={`text-sm font-medium tracking-wide transition-colors duration-200 ${
                  activeNav === link.label ? "text-teal-300" : "text-white/60 hover:text-white"
                }`}
              >
                {link.label}
              </button>
            </li>
          ))}
        </ul>
      </div>
      {menuOpen && (
        <ul className="md:hidden flex flex-col border-t border-white/10">
          {NAV_LINKS.map((link) => (
            <li key={link.label}>
              <button
                onClick={() => { setActiveNav(link.label); setMenuOpen(false); }}
                className={`block w-full text-left px-5 py-3 text-sm font-medium tracking-wide transition-colors duration-200 ${
                  activeNav === link.label ? "text-teal-300" : "text-white/60"
                }`}
              >
                {link.label}
              </button>
            </li>
          ))}
        </ul>
      )}
    </nav>
  );
}

const SECRET_PASSWORD = "ezv203";

function PasswordGate({ onUnlock }: { onUnlock: () => void }) {
  const [input, setInput] = useState("");
  const [error, setError] = useState(false);
  const [shake, setShake] = useState(false);

  const attempt = () => {
    if (input === SECRET_PASSWORD) {
      onUnlock();
    } else {
      setError(true);
      setShake(true);
      setTimeout(() => setShake(false), 500);
      setTimeout(() => setError(false), 2000);
      setInput("");
    }
  };

  return (
    <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-6">
      <p style={{ fontFamily: "'Fraunces', serif", fontStyle: "italic" }} className="text-white/30 text-sm mb-8 tracking-widest">
        this page is private
      </p>
      <div
        className={`flex flex-col items-center gap-4 w-full max-w-xs transition-transform ${shake ? "animate-[shake_0.4s_ease]" : ""}`}
        style={shake ? { animation: "shake 0.4s ease" } : {}}
      >
        <input
          type="password"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && attempt()}
          placeholder="password"
          className={`w-full bg-transparent border-b text-center text-white placeholder-white/20 text-lg py-2 outline-none tracking-widest transition-colors duration-300 ${error ? "border-red-500/60" : "border-white/20 focus:border-white/50"}`}
          style={{ fontFamily: "'Outfit', sans-serif" }}
          autoFocus
        />
        {error && <p className="text-red-400/70 text-xs tracking-wide">incorrect</p>}
        <button
          onClick={attempt}
          className="mt-2 text-white/40 hover:text-white text-xs tracking-widest uppercase transition-colors duration-200"
        >
          enter
        </button>
      </div>
      <style>{`@keyframes shake { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-8px)} 40%{transform:translateX(8px)} 60%{transform:translateX(-6px)} 80%{transform:translateX(6px)} }`}</style>
    </div>
  );
}

function SecretPage() {
  return (
    <div className="relative z-10 max-w-2xl mx-auto px-6 pt-16 pb-32 text-center">
      <h1 style={{ fontFamily: "'Fraunces', serif", fontStyle: "italic" }} className="text-5xl font-bold text-white mb-6">
        you found it.
      </h1>
      <p className="text-white/40 text-sm leading-relaxed">
        Add your secret content here.
      </p>
    </div>
  );
}

function HomePage({ onSecretClick }: { onSecretClick: () => void }) {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const onScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const titleOpacity = Math.max(0, 1 - scrollY / 120);
  const titleTranslate = scrollY * 0.5;
  const artOpacity = Math.max(0, 1 - scrollY / 200);
  const artTranslate = scrollY * 0.3;
  const textOpacity = Math.max(0, 1 - scrollY / 300);
  const textTranslate = scrollY * 0.15;

  return (
    <>
      {/* Hero photo background */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{ backgroundImage: `url(${heroPhoto})`, backgroundSize: "cover", backgroundPosition: "center", zIndex: 0 }}
      />
      <div
        className="fixed inset-0 pointer-events-none"
        style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.7) 35%, #000 55%)", zIndex: 1 }}
      />

      {/* Hero */}
      <section className="relative z-10 text-center px-6 min-h-[85vh]">
        <div className="flex flex-col items-center pt-[18vh]" style={{ opacity: titleOpacity, transform: `translateY(${titleTranslate}px)`, willChange: "opacity, transform" }}>
          <h1 style={{ fontFamily: "'Fraunces', serif", fontSize: "38px" }} className="font-bold tracking-tight text-white">
            Ezra Vernon
          </h1>
        </div>
        <div className="flex flex-col items-center mt-10" style={{ opacity: artOpacity, transform: `translateY(${artTranslate}px)`, willChange: "opacity, transform" }}>
          <img src={penguinArt} alt="Penguin on a surfboard illustration" className="object-contain" style={{ width: "151px", height: "151px" }} />
        </div>
        <p
          className="mx-auto mt-10 max-w-xl text-white/60 text-lg leading-relaxed px-6"
          style={{ opacity: textOpacity, transform: `translateY(${textTranslate}px)`, willChange: "opacity, transform" }}
        >
          Welcome to my page! Keep scrolling to learn more about me!
        </p>
      </section>

      {/* About */}
      <section className="relative z-10 max-w-2xl mx-auto px-6 pb-40 mt-[15vh]">
        <div className="p-8">
          <h2 style={{ fontFamily: "'Fraunces', serif" }} className="text-2xl font-bold text-teal-300 mb-5">about me</h2>
          <p className="text-white/70 leading-relaxed text-base mb-8">
            I love getting outside, exploring, making new friends, and stepping out of my comfort zone!
          </p>
          <p className="text-white/70 leading-relaxed text-base">
            My favourite sport is skiing, but I love ultimate frisbee, soccer, sport climbing, and ultra running as well
          </p>
        </div>
      </section>

      {/* Facts */}
      <section className="relative z-10 max-w-2xl mx-auto px-6 pb-40">
        <ul className="space-y-12">
          {FACTS.map((fact) => (
            <li key={fact.label} className="flex items-start gap-4 px-6 py-10">
              <div className="flex-1">
                <p className="text-white/40 text-xs uppercase tracking-widest font-medium mb-0.5">{fact.label}</p>
                <p className="text-white text-base font-medium">
                  {fact.href ? (
                    <a
                      href={fact.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline underline-offset-4 decoration-teal-300/60 hover:text-teal-300 transition-colors duration-200"
                    >
                      {fact.value}
                    </a>
                  ) : (
                    fact.value
                  )}
                </p>
                {fact.note && <p className="text-white/40 text-xs mt-0.5">{fact.note}</p>}
              </div>
            </li>
          ))}
        </ul>
      </section>

      {/* Mantra */}
      <section className="relative z-10 max-w-2xl mx-auto px-6 pb-44 text-center">
        <div className="relative p-10">
          <p className="text-white/30 text-xs uppercase tracking-widest mb-4 font-medium">Life Mantra</p>
          <blockquote style={{ fontFamily: "'Fraunces', serif", fontStyle: "italic" }} className="text-2xl md:text-3xl font-light text-white leading-snug">
            "Live in the balance between two Extremes."
          </blockquote>
        </div>
      </section>

      {/* Closing */}
      <section className="relative z-10 text-center px-6 pb-32">
        <p style={{ fontFamily: "'Fraunces', serif", fontStyle: "italic" }} className="text-white/30 text-lg mb-12">
          The End!
        </p>
        <button
          onClick={onSecretClick}
          className="fixed bottom-6 right-6 z-20 text-white/40 hover:text-white text-xs tracking-widest uppercase transition-colors duration-300"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          sign in
        </button>
      </section>
    </>
  );
}

function TrackerPage() {
  return (
    <>
      <div className="fixed inset-0 pointer-events-none" style={{ backgroundImage: `url(${trackerPhoto})`, backgroundSize: "cover", backgroundPosition: "center", zIndex: 0 }} />
      <div className="fixed inset-0 pointer-events-none" style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 60%, rgba(0,0,0,0.85) 100%)", zIndex: 1 }} />
    <div className="relative z-10 max-w-3xl mx-auto px-6 pt-16 pb-24">
      <h1 style={{ fontFamily: "'Fraunces', serif" }} className="text-4xl md:text-5xl font-bold text-white mb-16 text-center">
        What Am I Up To!?
      </h1>
      <p className="text-white/60 text-base leading-relaxed mb-10 max-w-xl text-center">
        These are trips and sidequests I have planned right now! Feel free to reach out to join an adventure!
      </p>

      {/* Legend */}
      <div className="flex flex-wrap gap-5 mb-10">
        {LEGEND.map((item) => (
          <div key={item.label} className="flex items-center gap-2">
            <span className={`w-3 h-3 rounded-full ${item.color}`} />
            <span className="text-white/60 text-sm">{item.label}</span>
          </div>
        ))}
      </div>

      {/* Calendar */}
      <div className="w-full overflow-hidden rounded-xl" style={{ aspectRatio: "4/3" }}>
        <iframe
          src="https://calendar.google.com/calendar/embed?src=f28275ef0df665f0edaecc11038705e4f686448d16250b43eef8e63bec594d5b%40group.calendar.google.com&ctz=America%2FVancouver"
          style={{ border: 0 }}
          width="100%"
          height="100%"
          frameBorder={0}
          scrolling="no"
          title="Ezra Locator"
        />
      </div>
    </div>
    </>
  );
}

const QUOTES = [
  { font: "'Lora', serif", style: "italic", size: "1.4rem" },
  { font: "'DM Serif Display', serif", style: "normal", size: "1.6rem" },
  { font: "'Playfair Display', serif", style: "italic", size: "1.3rem" },
  { font: "'Courier Prime', monospace", style: "normal", size: "1.15rem" },
  { font: "'Nunito', sans-serif", style: "normal", size: "1.35rem" },
  { font: "'Fraunces', serif", style: "italic", size: "1.5rem" },
  { font: "'Outfit', sans-serif", style: "normal", size: "1.25rem" },
];

const QUOTE_TEXTS = [
  "The difference between I, and another is a millimetre and a mile, all at the same time. Is this an illusion of difference? Or a signal of success within myself.",
  "The world is an infinite number of perspectives, each one waiting for something to see from them.",
  "What is Life's Purpose? The purpose of my life is to find the balance between the multitude of events and emotions throughout the inevitable course of my life and to live in the grey area of personal happiness.",
  "Life is like the ocean; although you can't control it, you can decide whether to sink or swim.",
  "Living in happiness sheds light on everything that is taken for granted.",
  "Confusion has a cost",
  "Live in the balance between two Extremes.",
];

function QuotesPage() {
  return (
    <>
      <div className="fixed inset-0 pointer-events-none" style={{ backgroundImage: "url('https://images.unsplash.com/photo-1508726989460-5741fe0304b3?w=1600&fit=crop&auto=format')", backgroundSize: "cover", backgroundPosition: "center", zIndex: 0 }} />
      <div className="fixed inset-0 pointer-events-none" style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.65) 35%, #000 65%)", zIndex: 1 }} />
    <div className="relative z-10 max-w-2xl mx-auto px-6 pt-16 pb-32">
      <h1
        style={{ fontFamily: "'Fraunces', serif" }}
        className="text-5xl font-bold text-white mb-4"
      >
        Quotes
      </h1>
      <p className="text-white/40 text-sm mb-32 tracking-wide leading-relaxed">
        These quotes, or daily reminders, are all original pieces written by me Enjoy!
      </p>

      <div className="space-y-24">
        {QUOTES.map((q, i) => (
          <div key={i} className="border-l-2 border-white/10 pl-8">
            <blockquote
              style={{ fontFamily: q.font, fontStyle: q.style, fontSize: q.size, lineHeight: 1.6 }}
              className="text-white/80 mb-3"
            >
              {QUOTE_TEXTS[i]}
            </blockquote>
            {q.attribution && (
              <p className="text-white/30 text-xs tracking-widest uppercase">{q.attribution}</p>
            )}
          </div>
        ))}
      <p className="text-center text-white/20 text-xs tracking-widest mt-16">
        more coming soon
      </p>
      </div>
    </div>
    </>
  );
}

function FutureDreamsPage() {
  return (
    <div className="relative z-10 max-w-2xl mx-auto px-6 pt-16 pb-24">
      <h1 style={{ fontFamily: "'Fraunces', serif" }} className="text-5xl font-bold text-white mb-16">
        Future Dreams
      </h1>

      {/* Climbing Goals title */}
      <div className="mb-4 px-2">
        <h2 style={{ fontFamily: "'Fraunces', serif" }} className="text-2xl font-bold text-teal-300">
          Climbing Goals
        </h2>
      </div>

      {/* Tetrahedron Peak */}
      <section className="mb-4 rounded-2xl px-7 py-6 overflow-hidden relative" style={{ backgroundImage: `url(${tetPeakPhoto})`, backgroundSize: "cover", backgroundPosition: "center" }}>
        <div className="absolute inset-0" style={{ background: "rgba(0,0,0,0.55)", backdropFilter: "blur(1px)" }} />
        <div className="relative z-10">
          <h3 style={{ fontFamily: "'Fraunces', serif" }} className="text-xl font-bold text-white mb-3">
            Tetrahedron Peak 2.0
          </h3>
          <ul className="text-white/70 text-sm space-y-1 leading-relaxed list-none pl-0">
            <li>Elevation: 1,739m — highest in the Tetrahedron</li>
            <li>Features a class S-4.1 scramble near the summit</li>
            <li>Already summited once in summer 2025</li>
            <li>Goal: return trip to overnight and witness sunrise/sunset at the top</li>
          </ul>
        </div>
      </section>

      {/* Mount Drew */}
      <section className="mb-4 rounded-2xl px-7 py-6 overflow-hidden relative" style={{ backgroundImage: `url(${mountDrewPhoto})`, backgroundSize: "cover", backgroundPosition: "center" }}>
        <div className="absolute inset-0" style={{ background: "rgba(0,0,0,0.55)", backdropFilter: "blur(1px)" }} />
        <div className="relative z-10">
          <h3 style={{ fontFamily: "'Fraunces', serif" }} className="text-xl font-bold text-white mb-3">
            Mount Drew
          </h3>
          <ul className="text-white/70 text-sm space-y-1 leading-relaxed list-none pl-0">
            <li>The notorious peak located in Squamish, BC.</li>
            <li>Elevation: 2,608m</li>
            <li>The highest peak, standing at a wild, 2,608 meters, it has always been a dream of mine to summit. It is one of the biggest glaciers in this region, making it very dangerous to climb and requiring mountaineering experience.</li>
            <li>The whole range spans 1,100,000 acres and has many peaks inside the area.</li>
          </ul>
        </div>
      </section>

      {/* Mount Tantalus */}
      <section className="mb-4 rounded-2xl px-7 py-6 overflow-hidden relative" style={{ backgroundImage: `url(${mtTantalusPhoto})`, backgroundSize: "cover", backgroundPosition: "center" }}>
        <div className="absolute inset-0" style={{ background: "rgba(0,0,0,0.55)", backdropFilter: "blur(1px)" }} />
        <div className="relative z-10">
          <h3 style={{ fontFamily: "'Fraunces', serif" }} className="text-xl font-bold text-white">
            Mount Tantalus
          </h3>
        </div>
      </section>

      {/* Mount Churchill */}
      <section className="mb-8 rounded-2xl px-7 py-6 overflow-hidden relative" style={{ backgroundImage: `url(${mountChurchillPhoto})`, backgroundSize: "cover", backgroundPosition: "center" }}>
        <div className="absolute inset-0" style={{ background: "rgba(0,0,0,0.55)", backdropFilter: "blur(1px)" }} />
        <div className="relative z-10">
          <h3 style={{ fontFamily: "'Fraunces', serif" }} className="text-xl font-bold text-white">
            Mount Churchill
          </h3>
        </div>
      </section>

      {/* Costco Ultra Marathon */}
      <section className="mb-8 rounded-2xl px-7 py-6" style={{ background: "rgba(20, 40, 50, 0.6)", backdropFilter: "blur(8px)" }}>
        <h2 style={{ fontFamily: "'Fraunces', serif" }} className="text-2xl font-bold text-teal-300 mb-3">
          Vancouver Costco Ultra Marathon
        </h2>
        <ul className="text-white/60 text-sm space-y-1 leading-relaxed list-none pl-0">
          <li>A 55.8 km route starting in Burnaby, going to Brentwood, downtown, Bridgeport, and Queensborough before ending back in Burnaby</li>
          <li>Rule: eat a Costco hot dog at all 5 Costcos</li>
          <li className="text-white/40 italic">Condiments are optional</li>
        </ul>
      </section>

      {/* Guitar */}
      <section className="mb-8 rounded-2xl px-7 py-6" style={{ background: "rgba(20, 40, 50, 0.6)", backdropFilter: "blur(8px)" }}>
        <h2 style={{ fontFamily: "'Fraunces', serif" }} className="text-2xl font-bold text-teal-300 mb-3">
          Guitar
        </h2>
        <p className="text-white/70 leading-relaxed">
          I want to learn how to play the guitar and get good enough that I can play for camping trips with friends.
        </p>
      </section>
    </div>
  );
}

const SOCIALS = [
  { name: "Instagram", handle: "@ezrav_insta", href: "https://www.instagram.com/ezrav_insta" },
  { name: "LinkedIn", handle: "Ezra Vernon", href: "https://www.linkedin.com/in/ezra-vernon-a98a40343/" },
  { name: "Strava", handle: "Follow my activities", href: "https://strava.app.link/lBou8jZCg7b" },
];

const NEON = "#ffb3d9";

function SocialsPage() {
  return (
    <>
      {/* Black marble with neon pink veins */}
      <div className="fixed inset-0 pointer-events-none bg-black" style={{ zIndex: 0 }}>
        <svg viewBox="0 0 400 800" preserveAspectRatio="xMidYMid slice" className="w-full h-full" aria-hidden="true">
          <defs>
            <filter id="veinGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" />
            </filter>
          </defs>
          <g fill="none" strokeLinejoin="round" strokeLinecap="round" stroke={NEON} filter="url(#veinGlow)" opacity="0.55">
            {VEINS.map((v, i) => <path key={i} d={v.d} strokeWidth={v.w * 2.5} />)}
          </g>
          <g fill="none" strokeLinejoin="round" strokeLinecap="round" stroke={NEON}>
            {VEINS.map((v, i) => <path key={i} d={v.d} strokeWidth={v.w} opacity={v.o} />)}
          </g>
        </svg>
      </div>
      <div className="fixed inset-0 pointer-events-none" style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.2) 70%)", zIndex: 1 }} />

      <div className="relative z-10 max-w-md mx-auto px-6 pt-16 pb-32">
        <h1
          style={{ fontFamily: "'Fraunces', serif", color: "#ffe3f1", textShadow: `0 0 8px ${NEON}, 0 0 24px ${NEON}, 0 0 48px #ff6fb5` }}
          className="text-5xl font-bold mb-16 text-center"
        >
          socials
        </h1>
        <ul className="space-y-8">
          {SOCIALS.map((s) => (
            <li key={s.name}>
              <a
                href={s.href}
                target="_blank"
                rel="noopener noreferrer"
                className="block rounded-2xl px-7 py-6 bg-black/60 transition-all duration-300 hover:bg-black/80 hover:scale-[1.02]"
                style={{ border: `1.5px solid ${NEON}`, boxShadow: `0 0 10px ${NEON}66, inset 0 0 12px ${NEON}22` }}
              >
                <p style={{ fontFamily: "'Fraunces', serif", color: "#ffe3f1", textShadow: `0 0 10px ${NEON}` }} className="text-2xl font-bold">
                  {s.name}
                </p>
                <p className="text-sm mt-1" style={{ color: `${NEON}cc` }}>{s.handle}</p>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default function App() {
  const [activeNav, setActiveNav] = useState("Home");
  const [menuOpen, setMenuOpen] = useState(false);
  const [secretState, setSecretState] = useState<"hidden" | "gate" | "unlocked">("hidden");

  const handleSecretClick = () => setSecretState("gate");
  const handleUnlock = () => setSecretState("unlocked");

  return (
    <div style={{ fontFamily: "'Outfit', sans-serif" }} className="min-h-full bg-black text-white overflow-x-hidden">
      <Nav activeNav={activeNav} setActiveNav={(v) => { setActiveNav(v); setSecretState("hidden"); }} menuOpen={menuOpen} setMenuOpen={setMenuOpen} />

      {secretState === "gate" && <PasswordGate onUnlock={handleUnlock} />}
      {secretState === "unlocked" && <SecretPage />}
      {secretState === "hidden" && (
        <>
          {activeNav === "Home" && <HomePage onSecretClick={handleSecretClick} />}
          {activeNav === "Ezra Tracker" && <TrackerPage />}
          {activeNav === "Future Dreams" && <FutureDreamsPage />}
          {activeNav === "Quotes" && <QuotesPage />}
          {activeNav === "Socials" && <SocialsPage />}
        </>
      )}

      <footer className="relative z-10 py-6 text-center">
        <p className="text-white/20 text-xs tracking-wide">
          Ezra Vernon &middot; {new Date().getFullYear()}
        </p>
      </footer>
    </div>
  );
}
