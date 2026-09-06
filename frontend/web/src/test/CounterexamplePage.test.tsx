import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it, vi } from 'vitest';
import { emptyMissionView } from '../../../core/src/missionView';
import { CounterexamplePage } from '../research-workbench/pages/CounterexamplePage';
import type { WorkspacePageProps } from '../research-workbench/pages/pageTypes';
import type { CounterexampleCandidate } from '../research-workbench/types';

vi.mock('../research-workbench/useWorkbenchText', () => ({
  useWorkbenchText: () => ({ text: (_zh: string, en: string) => en }),
}));

function page(missionStatus: string, candidateStatus = 'queued') {
  const mission = emptyMissionView();
  mission.mission.title = 'Investigate 10';
  mission.mission.status = missionStatus;
  const candidates = ['1', '10'].map((id): CounterexampleCandidate => ({
    id,
    title: `Candidate ${id}`,
    description: '',
    classification: '',
    source_grade: '',
    verification_level: '',
    status: candidateStatus,
    progress: 8,
    disposition: '',
    result_summary: '',
    rejection_reason: '',
    evidence_path: '',
    parallel_files: 0,
    updated_at: Date.now(),
  }));
  return {
    snapshot: { mission_view: mission, backlog: [] },
    counterexamples: {
      schema_version: 1, generated_at: Date.now(), total: 2, counts: {}, candidates,
    },
    connected: true,
  } as WorkspacePageProps;
}

describe('CounterexamplePage live projection', () => {
  it('matches whole candidate IDs instead of marking 1 active when working on 10', () => {
    const html = renderToStaticMarkup(<CounterexamplePage {...page('working')} />);
    expect((html.match(/data-active="true"/g) ?? []).length).toBe(1);
    expect(html).toContain('Investigate 10');
  });

  it('does not project a completed mission as current activity', () => {
    const html = renderToStaticMarkup(<CounterexamplePage {...page('completed')} />);
    expect(html).not.toContain('data-active="true"');
    expect(html).not.toContain('Now working');
  });

  it('does not revive a terminal candidate as active', () => {
    const html = renderToStaticMarkup(<CounterexamplePage {...page('working', 'verified')} />);
    expect(html).not.toContain('data-active="true"');
    expect(html).toContain('Refuted');
  });

  it('does not treat old construction artifacts as a currently running mission', () => {
    const html = renderToStaticMarkup(<CounterexamplePage {...page('completed', 'constructing')} />);
    expect(html).not.toContain('data-active="true"');
    expect(html).not.toContain('Now working');
  });
});
