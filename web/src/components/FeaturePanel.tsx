type FeaturePanelProps = {
  eyebrow: string;
  title: string;
  features: string[];
  proofPoints: string[];
};

export default function FeaturePanel({ eyebrow, title, features, proofPoints }: FeaturePanelProps) {
  return (
    <section className="feature-panel">
      <span className="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      <div className="feature-columns">
        <div className="feature-group">
          <h3>Core moves</h3>
          <ul className="feature-list">
            {features.map((entry) => (
              <li key={entry}>{entry}</li>
            ))}
          </ul>
        </div>
        <div className="feature-group">
          <h3>Proof markers</h3>
          <ul className="feature-list feature-proof-list">
            {proofPoints.map((entry) => (
              <li key={entry}>{entry}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
