import { TestBed } from '@angular/core/testing';
import { IndexComponent } from './index.component';

describe('IndexComponent', () => {
  it('should render the index page with the information text', () => {
    const fixture = TestBed.createComponent(IndexComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    fixture.detectChanges();
    expect(compiled.querySelector('div.index h1')?.textContent)
      .toContain('Schedule');
  });
});
