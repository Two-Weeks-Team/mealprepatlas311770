type HeroProps = {
  appName: string;
  tagline: string;
  proofPoints: string[];
  eyebrow: string;
  visualSrc: string;
};

export default function Hero({ appName, tagline, proofPoints, eyebrow, visualSrc }: HeroProps) {
  return (
    <section className="hero">
      <div className="hero-copy">
        <span className="eyebrow">{eyebrow}</span>
        <h1>{appName}</h1>
        <p>{tagline}</p>
        <ul className="hero-proof-list">
          {proofPoints.map((point) => (
            <li className="proof-pill" key={point}>{point}</li>
          ))}
        </ul>
      </div>
      <div className="hero-visual-frame">
        <img className="hero-visual" src={visualSrc} alt={`${appName} visual`} />
      </div>
    </section>
  );
}
