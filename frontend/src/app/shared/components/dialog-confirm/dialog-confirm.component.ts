import { Component, EventEmitter, Input, Output } from '@angular/core'


@Component( {
    selector: 'app-dialog-confirm',
    templateUrl: './dialog-confirm.component.html',
    styleUrls: [ './dialog-confirm.component.scss' ]
} )
export class DialogConfirmComponent
{
    @Input() modalVisible!: boolean
    @Input() dialogMessage!: string
    @Input() actionConfirmText!: string
    @Output() actionConfirmed: EventEmitter<void> = new EventEmitter<void>()
    @Output() actionCanceled: EventEmitter<void> = new EventEmitter<void>()

    confirmClicked(): void
    {
        this.actionConfirmed.emit()
    }

    cancelClicked(): void
    {
        this.actionCanceled.emit()
    }
}
