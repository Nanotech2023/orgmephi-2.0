import { Component, EventEmitter, Input, Output } from '@angular/core'
import { DocumentForeignPassport } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-document-foreignpassport',
    templateUrl: './profile-edit-document-foreignpassport.component.html',
    styleUrls: [ './profile-edit-document-foreignpassport.component.scss' ]
} )
export class ProfileEditDocumentForeignpassportComponent
{
    @Input() model!: DocumentForeignPassport
    @Output() modelChange = new EventEmitter<DocumentForeignPassport>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}
