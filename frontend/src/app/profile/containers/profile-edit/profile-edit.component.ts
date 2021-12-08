import { Component } from '@angular/core'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'


@Component( {
    selector: 'app-profile-edit',
    templateUrl: './profile-edit.component.html',
    styleUrls: [ './profile-edit.component.scss' ]
} )
export class ProfileEditComponent
{
    constructor( private store: Store<AuthState.State> )
    {
    }

    download(): void
    {
        this.store.select( AuthSelectors.selectUserPhoto ).subscribe( data => this.downloadFile( data ) )
    }

    downloadFile( data: Blob ): void
    {
        const blob = new Blob( [ data ], { type: 'application/pdf' } )
        const url = window.URL.createObjectURL( blob )
        window.open( url )
    }
}