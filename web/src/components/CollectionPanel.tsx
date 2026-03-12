type SavedPlan = {
  summary: string;
  score: number;
  items: Array<{ title: string; detail: string; score: number }>;
};

export default function CollectionPanel({
  saved,
  eyebrow,
  title,
  emptyTitle,
  emptyDetail,
}: {
  saved: SavedPlan[];
  eyebrow: string;
  title: string;
  emptyTitle: string;
  emptyDetail: string;
}) {
  return (
    <section className="collection-panel">
      <div className="section-heading">
        <span className="eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
      </div>
      <div className="saved-grid">
        {saved.length ? (
          saved.map((entry, index) => (
            <article className="saved-card" key={`${entry.summary}-${index}`}>
              <span className="saved-score">Score {entry.score}</span>
              <h3>{entry.summary}</h3>
              <ul>
                {entry.items.slice(0, 2).map((item) => (
                  <li key={item.title}>{item.title}</li>
                ))}
              </ul>
            </article>
          ))
        ) : (
            <article className="saved-card">
              <span className="saved-score">Empty state</span>
              <h3>{emptyTitle}</h3>
              <p>{emptyDetail}</p>
           </article>
        )}
      </div>
    </section>
  );
}
