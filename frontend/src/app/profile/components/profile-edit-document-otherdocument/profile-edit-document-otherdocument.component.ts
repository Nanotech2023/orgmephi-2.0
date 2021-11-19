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

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}
