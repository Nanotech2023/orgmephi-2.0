import { Component, EventEmitter, Output } from '@angular/core'


@Component( {
    selector: 'app-header-confirm-account',
    templateUrl: './header-confirm-account.component.html',
    styleUrls: [ './header-confirm-account.component.scss' ]
} )
export class HeaderConfirmAccountComponent
{
    @Output() closeHeader = new EventEmitter<boolean>()

    onClose()
    {
        this.closeHeader.emit( true )
    }
}