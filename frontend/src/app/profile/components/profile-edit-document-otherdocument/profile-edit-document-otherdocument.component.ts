import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { DocumentOther } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-document-otherdocument',
    templateUrl: './profile-edit-document-otherdocument.component.html',
    styleUrls: [ './profile-edit-document-otherdocument.component.scss' ]
} )
export class ProfileEditDocumentOtherdocumentComponent
{
    @Input() model!: DocumentOther
    @Output() modelChange = new EventEmitter<DocumentOther>()

    numberPattern: string = "^[0-9]{1,32}$"
    seriesPattern: string = "^[0-9]{1,16}$"

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}
