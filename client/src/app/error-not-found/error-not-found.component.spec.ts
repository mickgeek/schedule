import { TestBed } from '@angular/core/testing';
import { ErrorNotFoundComponent } from './error-not-found.component';

describe('ErrorNotFoundComponent', () => {
  it('should render the not found error', () => {
    const fixture = TestBed.createComponent(ErrorNotFoundComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;
    fixture.detectChanges();
    expect(compiled.querySelector('div.error-not-found h1')?.textContent).toContain('Error 404');
  });
});
