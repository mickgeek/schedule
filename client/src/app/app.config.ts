import { InjectionToken } from '@angular/core';
import { environment } from '../environments/environment';

export interface AppConfig {
  production: boolean,
  beginningDate: string,
  serverEndpoint: string
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');
export const ENVIRONMENT: AppConfig = environment;
