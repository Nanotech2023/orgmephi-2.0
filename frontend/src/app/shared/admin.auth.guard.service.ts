import { Injectable } from '@angular/core'
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'


@Injectable()
export class AdminAuthGuardService implements CanActivate
{
    constructor( private store: Store<AuthState.State>, private router: Router ) {}

    canActivate( route: ActivatedRouteSnapshot, state: RouterStateSnapshot ): Observable<boolean> | Promise<boolean> | boolean
    {
        return this.store.pipe( select( AuthSelectors.selectIsPrivileged ),
            map( isPrivileged =>
            {
                if ( isPrivileged )
                    this.router.navigate( [ '/' ] )
                return isPrivileged
            } ) )
    }
}