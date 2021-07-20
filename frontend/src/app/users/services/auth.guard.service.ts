import { Injectable } from '@angular/core'
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router'
import { Observable } from 'rxjs'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { map } from 'rxjs/operators'


@Injectable()
export class AuthGuardService implements CanActivate
{
    constructor( private store: Store<AuthState.State>, private router: Router ) {}

    canActivate( route: ActivatedRouteSnapshot, state: RouterStateSnapshot ): Observable<boolean> | Promise<boolean> | boolean
    {
        return this.store.pipe(
            select( AuthSelectors.selectIsAuthenticated ),
            map( authorized =>
            {
                if ( !authorized )
                    this.router.navigate( [ '' ] )
                return authorized
            } ) )
    }
}